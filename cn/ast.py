from abc import ABCMeta, abstractmethod
from llvm import *
from llvm.core import *
from cn.libcn import LibCN

llvmTypes = {
    'INT': Type.int(),
    'FLOAT': Type.double(),
    'BOOLEAN' : Type.int(1),
    'VOID' : Type.void(),
    'STRING' : Type.pointer(Type.int(8))
    }

# Helper method for creating allocations of variables on the stack
def createEntryBlockAlloca(function, dataType, var_name):
  entry = function.get_entry_basic_block()
  builder = Builder.new(entry)
  builder.position_at_beginning(entry)
  return builder.alloca(llvmTypes[dataType], name=var_name)

class SyntaxNode(object):
  __metaclass__ = ABCMeta

  @abstractmethod
  def codeGen(self):
    pass

class Program(SyntaxNode):
  def __init__(self, imports, declarations):
    if imports == None:
      imports = []
    self.imports = imports
    self.declarations = declarations

  def codeGen(self, name):
    module = Module.new(name)
    scope = {'module': module, 'parent': None, 'names': {}}

    for importDec in self.imports:
      importDec.codeGen(scope)

    func = module.get_or_insert_function(LibCN().printf, 'printf')
    scope['names']['printf'] = func, 'FUNC', 'INT'
    
    func = module.get_or_insert_function(LibCN().scanf, 'scanf')
    scope['names']['scanf'] = func, 'FUNC', 'INT'
    
    func = module.get_or_insert_function(LibCN().getchar, 'getchar')
    scope['names']['getchar'] = func, 'FUNC', 'INT'
    
    func = module.get_or_insert_function(LibCN().system, 'system')
    scope['names']['system'] = func, 'FUNC', 'INT'
    
    for declaration in self.declarations:
      declaration.codeGen(scope)
    module.verify()
    return module

class ImportDeclaration(SyntaxNode):
  def __init__(self, importID):
    self.name = importID

  def codeGen(self, scope):
    pass

class GVariableDeclaration(SyntaxNode):
  def __init__(self, typeSpec, name, expression=None):
    self.typeSpec = typeSpec.upper()
    self.name = name
    self.expression = expression
 
  def codeGen(self, scope):
    vc = scope['module'].add_global_variable(llvmTypes[self.typeSpec], self.name)
    if self.expression != None:
      val, typeSpec = self.expression.codeGen(scope)
      if typeSpec != self.typeSpec:
        raise RuntimeException("Global variable type of %s does not match %s" % self.name, typeSpec) 
      vc.initializer = val
      vc.linkage = LINKAGE_LINKONCE_ODR
    scope['names'][self.name] = (vc, self.type)

    return vc, self.type

class Variable(SyntaxNode):
  def __init__(self, name, index=None):
    self.name = name
    self.index = index

  def codeGen(self, scope):
    if self.index == None:
      currScope = scope

      while currScope != None:
        if self.name in currScope['names']:
          identifier = currScope['names'][self.name]
          if type(identifier[0]) == llvm.core.Argument:
            return identifier
          elif identifier[1] == "FUNC":
            return identifier
          else:
            return scope['builder'].load(identifier[0], self.name), identifier[1]
        currScope = currScope['parent']
      return None, None
    else:
      currscope = scope
      index = self.index.codeGen(scope)
      while currscope != None:
        if self.name in currscope['names']:
          identifier = currscope['names'][self.name]
          if type(identifier[0]) == llvm.core.AllocaInstruction:
            ptr = scope['builder'].gep(identifier[0],[index[0]])
            return scope['builder'].load(ptr), identifier[2]
        currscope = currscope['parent']
      return None, None

class Function(SyntaxNode):
  def __init__(self, typeSpec, name, params, body):
    self.typeSpec = typeSpec.upper()
    self.name = name
    if params == None:
      params = []
    self.params = params
    self.body = body

  def codeGen(self, scope):
    newScope = {'module' : scope['module'], 'parent' : scope, 'names' : {}}
    params = [param.codeGen(scope) for param in self.params]
    funcType = Type.function(llvmTypes[self.typeSpec], params)
    
    func = scope['module'].add_function(funcType, self.name)
    scope['names'][self.name] = (func, 'FUNC', self.typeSpec)
    for arg, param in zip(func.args, self.params):
      arg.name = param.name
      scope['names'][param.name] = (arg, param.typeSpec)

    bb = func.append_basic_block("entry")
    newScope['builder'] = Builder.new(bb)
    try:
      for statement in self.body:
        statement.codeGen(newScope)
      if(self.typeSpec == 'VOID'):
        newScope['builder'].ret_void()
      func.verify()
    except:
      func.delete()
      raise

    return funcType, self.typeSpec

class Array(SyntaxNode) :
  def __init__(self,value) :
    self.value = value
  def codeGen(self, scope) :
    pass

    
class Param(SyntaxNode):
  def __init__(self, typeSpec, name):
    self.typeSpec = typeSpec.upper()
    self.name = name

  def codeGen(self, scope):
    return llvmTypes[self.typeSpec]

class ClassDeclaration(SyntaxNode):
  def __init__(self, name, body):
    self.type = 'class'
    self.name = name
    self.body = body

  def codeGen(self, scope):
    pass

class IfStmt(SyntaxNode):
  def __init__(self, condition, statement):
    self.condition = condition
    self.statement = statement

  def codeGen(self, scope):
    condition, dtype = self.condition.codeGen(scope)
    if dtype != "BOOLEAN":
      raise RuntimeError('If expression is not boolean')

    function = scope['builder'].basic_block.function

    then_block = function.append_basic_block('then')
    end_block= function.append_basic_block('endif')

    scope['builder'].cbranch(condition, then_block, end_block)

    scope['builder'].position_at_end(then_block)
    then_value = [s.codeGen(scope) for s in self.statement]
    scope['builder'].branch(end_block)

    scope['builder'].position_at_end(end_block)


class IfElseStmt(SyntaxNode):
  def __init__(self, condition, statement1, statement2):
    self.condition = condition
    self.statement1 = statement1
    self.statement2 = statement2

  def codeGen(self, scope):
    condition, dtype = self.condition.codeGen(scope)
    if dtype != "BOOLEAN":
      raise RuntimeError('If expression is not boolean')

    function = scope['builder'].basic_block.function

    then_block = function.append_basic_block('then')
    else_block = function.append_basic_block('else')
    end_block= function.append_basic_block('endif')

    scope['builder'].cbranch(condition, then_block, else_block)

    scope['builder'].position_at_end(then_block)
    then_value = [s.codeGen(scope) for s in self.statement1]
    scope['builder'].branch(end_block)

    scope['builder'].position_at_end(else_block)
    else_value = [s.codeGen(scope) for s in self.statement2]
    scope['builder'].branch(end_block)

    scope['builder'].position_at_end(end_block)

class WhileStmt(SyntaxNode):
  def __init__(self, condition, statement):
    self.condition = condition
    self.statement = statement

  def codeGen(self, scope):
    condition, dtype = self.condition.codeGen(scope)
    if dtype != "BOOLEAN":
      raise RuntimeError('If expression is not boolean')
    
    
    function = scope['builder'].basic_block.function
    
    then_block = function.append_basic_block('then')
    end_block= function.append_basic_block('endwhile')

    scope['builder'].cbranch(condition, then_block, end_block)

    scope['builder'].position_at_end(then_block)
    then_value = [s.codeGen(scope) for s in self.statement]
    condition, dtype = self.condition.codeGen(scope)
    scope['builder'].cbranch(condition, then_block, end_block)
    #scope['builder'].branch(end_block)

    scope['builder'].position_at_end(end_block)

class ReturnStmt(SyntaxNode):
  def __init__(self, expression=None):
    self.expression = expression

  def codeGen(self, scope):
    if self.expression == None:
      scope['builder'].ret_void()
    else:
      result = self.expression.codeGen(scope)
      scope['builder'].ret(result[0])

class VariableDeclaration(SyntaxNode):
  def __init__(self, typeSpec, name, expression=None):
    self.typeSpec = typeSpec.upper()
    self.name = name
    self.expression = expression

  def codeGen(self, scope):
    if self.expression == None:
      # Handle declaration
      pass
    else:
      value, typeSpec = self.expression.codeGen(scope)
      if typeSpec != self.typeSpec:
        # Not the same type
        raise RuntimeEerror("Not the same type")
      alloca = createEntryBlockAlloca(scope['builder'].basic_block.function, self.typeSpec, self.name)
      scope['builder'].store(value, alloca)
      scope['names'][self.name] = (alloca, self.typeSpec)

      return alloca, None

class ArrayDeclaration(SyntaxNode):
  def __init__(self, typeSpec, name, size, array_lit=None):
    self.typeSpec = typeSpec.upper()
    self.name = name
    self.size = size
    self.array_lit = array_lit

  def codeGen(self, scope):
    size = Constant.int(Type.int(), self.size)
    arr = scope['builder'].alloca(llvmTypes[self.typeSpec], size, self.name)
    scope['names'][self.name] = (arr, 'ARRAY', self.typeSpec)
    return arr, 'ARRAY'

class Assignment(SyntaxNode):
  def __init__(self, variable, expression, indexExpression=None):
    self.variable = variable
    self.expression = expression
    self.indexExpression = indexExpression

  def codeGen(self, scope):
    value, typeSpec = self.expression.codeGen(scope)
    
    variable = None
    currScope = scope
    while currScope != None:
      if self.variable in currScope['names']:
          variable = currScope['names'][self.variable]
      currScope = currScope['parent']
   
    if variable == None:
      # error, variable not found in scope
      raise RuntimeError("No variable named %s" % self.variable)
    if self.indexExpression == None: 
      scope['builder'].store(value, variable[0])
    else:
      index = self.indexExpression.codeGen(scope)
      if type(variable[0]) == llvm.core.AllocaInstruction:
        ptr = scope['builder'].gep(variable[0],[index[0]])
        scope['builder'].store(value, ptr)
    return value

class Integer(SyntaxNode):
  def __init__(self, value):
    self.value = value

  def codeGen(self, scope):
    ty = Type.int()
    val = Constant.int(ty, self.value)
    #tmp = scope['builder'].add(val, Constant.int(ty, 0), "tmp")
    return val, 'INT'

class Float(SyntaxNode):
  def __init__(self, value):
    self.value = value

  def codeGen(self, scope):
    ty = Type.double()
    val = Constant.real(ty, self.value)
    #tmp = scope['builder'].fadd(val, Constant.real(ty, 0.0), "tmp")
    return val, 'FLOAT'


class Boolean(SyntaxNode):
  def __init__(self, value):
    self.value = value

  def codeGen(self, scope):
    ty = Type.int(1)
    val = Constant.int(ty, self.value)
    #tmp = scope['builder'].add(val, Constant.int(ty, 0), "tmp")
    return val, 'BOOLEAN'

class String(SyntaxNode):
  def __init__(self, value):
    self.value = value

  def codeGen(self, scope):
    ty = Type.pointer(Type.int(8))
    val = Constant.stringz(self.value)
    tmp = scope['builder']
    collision = 0
    mod = scope['module']
    name_fmt = '.conststr.%x.%x'
    while True:
      name = name_fmt % (hash(self.value), collision)
      try:
        globalstr = mod.get_global_variable_named(name)
      except LLVMException:
        globalstr = mod.add_global_variable(val.type, name=name)
        globalstr.initializer = val
        globalstr.linkage = LINKAGE_LINKONCE_ODR
        globalstr.global_constant = True
      else:
        existed = str(globalstr.initializer)
        if existed != str(val):
          collision += 1
          continue
      return globalstr.bitcast(Type.pointer(val.type.element)), 'STRING'

class Character(SyntaxNode):
  def __init__(self, value):
    self.value = value

  def codeGen(self, scope):
    pass

opResultType = {
    '+': 'INT',
    '-': 'INT', 
    '*': 'INT',
    '/': 'INT',
    '%': 'INT',
    '==': 'BOOLEAN',
    '<=': 'BOOLEAN',
    '<': 'BOOLEAN',
    '>=': 'BOOLEAN',
    '>': 'BOOLEAN',
    '+f': 'FLOAT',
    '-f': 'FLOAT',
    '*f': 'FLOAT',
    '/f': 'FLOAT',
    '%f': 'FLOAT',
    '==b': 'BOOLEAN',
    '&&b': 'BOOLEAN',
    '||b': 'BOOLEAN'
}

class BinaryOp(SyntaxNode):
  def __init__(self, left, op, right):
    self.type = "binop"
    self.left = left
    self.right = right
    self.op = op

  def codeGen(self,scope):
    left = self.left.codeGen(scope)
    right = self.right.codeGen(scope)
    assert(left[1] == right[1])
    op = self.op
    if(left[1] == 'INT') :
      op = self.op
    elif(left[1] == 'FLOAT') :
      op += 'f'
    elif(left[1] == 'BOOLEAN') :
      op += 'b'
    builder = scope['builder']
    tmp = {'+': lambda l, r: builder.add(l, r, "tmp"),
        '-': lambda l, r: builder.sub(l, r, "tmp"),
        '*': lambda l, r: builder.mul(l, r, "tmp"),
        '/': lambda l, r: builder.sdiv(l, r, "tmp"),
        '%': lambda l, r: builder.srem(l, r, "tmp"),
        '==': lambda l, r: builder.icmp(ICMP_EQ, l, r, "tmp"),
        '>=': lambda l, r: builder.icmp(ICMP_SGE, l, r, "tmp"),
        '>': lambda l, r: builder.icmp(ICMP_SGT, l, r, "tmp"),
        '<=': lambda l, r: builder.icmp(ICMP_SLE, l, r, "tmp"),
        '<': lambda l, r: builder.icmp(ICMP_SLT, l, r, "tmp"),
        '+f': lambda l, r: builder.fadd(l, r, "tmp"),
        '-f': lambda l, r: builder.fsub(l, r, "tmp"),
        '*f': lambda l, r: builder.fmul(l, r, "tmp"),
        '/f': lambda l, r: builder.fdiv(l, r, "tmp"),
        '%f': lambda l, r: builder.frem(l, r, "tmp"),
        '==b': lambda l, r: builder.icmp(ICMP_EQ, l, r, "tmp"),
        '&&b': lambda l, r: builder.and_(l, r, "tmp"),
        '||b': lambda l, r: builder.or_(l, r, "tmp")
        }
    return tmp[op](left[0], right[0]), opResultType[op];

class UnaryOp(SyntaxNode):
  def __init__(self, op, expression):
    self.op = op
    self.expression = expression

  def codeGen(self, scope):
    pass

class Call(SyntaxNode):
  def __init__(self, expression, arguments):
    self.expression = expression 
    if arguments == None:
      arguments = []
    self.arguments = arguments

  def codeGen(self, scope):
    func = self.expression.codeGen(scope)
    if func[1] != "FUNC":
      raise RuntimeError("Not a function")
    
    #if len(func.args) != len(self.arguments):
    #  raise RuntimeError("Incorrect number of arguments")
    len(self.arguments)
    argvalues = [i.codeGen(scope)[0] for i in self.arguments]
    return scope['builder'].call(func[0], argvalues, 'calltmp'), func[2]
