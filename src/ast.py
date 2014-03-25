from abc import ABCMeta, abstractmethod
from llvm import *
from llvm.core import *

llvmTypes = {
    'INT': Type.int(),
    'FLOAT': Type.float(),
    'BOOLEAN' : Type.int(8),
    'VOID' : Type.void()
    }

# Helper method for creating allocations of variables on the stack
def createEntryBlockAlloca(function, dataType, var_name):
  entry = function.get_entry_basic_block()
  builder = Builder.new(entry)
  builder.position_at_beginning(entry)
  return builder.alloca(llvmTypes[dataType], var_name)

class SyntaxNode(object):
  __metaclass__ = ABCMeta

  @abstractmethod
  def codeGen(self):
    pass

class Program(SyntaxNode):
  def __init__(self, imports, declarations):
    self.imports = imports
    self.declarations = declarations

  def codeGen(self, name):
    module = Module.new(name)
    scope = {'module': module, 'parent': None, 'names': {}}
    for importDec in self.imports:
      importDec.codeGen(scope)

    for declaration in self.declarations:
      declaration.codeGen(scope)

    return module

class ImportDeclaration(SyntaxNode):
  def __init__(self, importID):
    self.name = importID

  def codeGen(self, scope):
    pass

class GVariableDeclaration(SyntaxNode):
  def __init__(self, typeSpec, name, expression=None):
    self.type = typeSpec
    self.name = name
 
  def codeGen(self, scope):
    vc = scope['module'].add_global_variable(llvmTypes[self.typeSpec], self.name)
    #TODO assign value to variable 
    scope['names'][self.name] = vc

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
          return scope['builder'].load(currScope['names'][self.name], self.name)
      return None
    else:
      #Handle array reference
      return None

class Function(SyntaxNode):
  def __init__(self, typeSpec, name, params, body):
    self.typeSpec = typeSpec
    self.name = name
    self.params = params
    self.body = body

  def codeGen(self, scope):
    newScope = {'module' : scope['module'], 'parent' : scope, 'names' : {}}
    params = [param.codeGen() for param in self.params]
    funcType = Type.function(llvmType[self.typeSpec], params)
    
    func = scope['module'].add_function(funcType, self.name)
    
    for arg, param in zip(func.args, self.params):
      arg.name = param.name
      scope['names'][param.name] = arg


    bb = func.append_basic_block("entry")
    newScope['builder'] = Builder.new(bb)
    try: 
      body = self.body.codeGen(newScope)
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
    self.type = typeSpec
    self.name = name

  def codeGen(self, scope):
    return llvmTypes[self.type]   

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
    condition, dtype = self.condition.codeGen()

    if dtype != "BOOLEAN":
      #TODO some error
      raise error('If expression is not boolean')

    # Convert to llvm bool

    # Create block and branch

class IfElseStmt(SyntaxNode):
  def __init__(self, condition, statement1, statement2):
    self.condition = condition
    self.statement1 = statement1
    self.statement2 = statement2

  def codeGen(self, scope):
    condition = self

class WhileStmt(SyntaxNode):
  def __init__(self, condition, statement):
    self.condition = condition
    self.statement = statement

  def codeGen(self, scope):
    pass

class ReturnStmt(SyntaxNode):
  def __init__(self, expression):
    self.expression = expression

  def codeGen(self, scope):
    result = self.expression.codeGen(scope)
    scope['builder'].ret(result)

class VariableDeclaration(SyntaxNode):
  def __init__(self, typeSpec, name, expression=None):
    self.typeSpec = typeSpec
    self.name = name
    self.expression = expression

  def codeGen(self, scope):
    if self.expression == None:
      # Handle declaration
      pass
    else:
      value, typeSpec = expression.codeGen()
      if typeSpec != self.typeSpec:

        # Not the same type
        raise Error("Not the same type")
      alloca = createEntryBlockAlloca(scope['builder'].basic_block.function, self.typeSpec, self.name)
      scope['builder'].store(value, alloca)
      scope['names'] = alloca

      return alloca, None

class Assignment(SyntaxNode):
  def __init__(self, variable, expression):
    self.variable = variable
    self.expression = expression

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
      raise Error("No variable named " + self.variable)
      
    scope['builder'].store(value, variable)

    return value

class Integer(SyntaxNode):
  def __init__(self, value):
    self.value = value

  def codeGen(self, scope):
    ty = Type.int()
    val = Constant.int(ty, self.value)
    tmp = scope.add(val, Constant.int(ty, 0), "tmp")
    return tmp, 'INT'

class Float(SyntaxNode):
  def __init__(self, value):
    self.value = value

  def codeGen(self, scope):
    ty = Type.float()
    val = Constant.real(ty, self.value)
    tmp = scope.add(val, Constant.real(ty, 0), "tmp")
    return tmp, 'FLOAT'


class Boolean(SyntaxNode):
  def __init__(self, value):
    self.value = value

  def codeGen(self, scope):
    ty = Type.int(8)
    val = Constant.int(ty, self.value)
    tmp = scope.add(val, Constant.int(ty, 0), "tmp")
    return tmp, 'INT'

class String(SyntaxNode):
  def __init__(self, value):
    self.value = value

  def codeGen(self, scope):
    pass

class Character(SyntaxNode):
  def __init__(self, value):
    self.value = value

  def codeGen(self, scope):
    pass

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
    if(left[1] == 'INT') :
      self.op
    elif(left[1] == 'FLOAT') :
      self.op += 'f'
    elif(left[1] == 'BOOLEAN') :
      self.op += 'b'
    tmp = {'+': lambda l, r: scope.add(l, r, "tmp"),
        '-': lambda l, r: scope.sub(l, r, "tmp"),
        '*': lambda l, r: scope.mul(l, r, "tmp"),
        '/': lambda l, r: scope.sdiv(l, r, "tmp"),
        '%': lambda l, r: scope.srem(l, r, "tmp"),
        '==': lambda l, r: scope.icmp(ICMP_EQ, l, r, "tmp"),
        '<=': lambda l, r: scope.icmp(ICMP_SGE, l, r, "tmp"),
        '<': lambda l, r: scope.icmp(ICMP_SGT, l, r, "tmp"),
        '>=': lambda l, r: scope.icmp(ICMP_SLE, l, r, "tmp"),
        '>': lambda l, r: scope.icmp(ICMP_SLT, l, r, "tmp"),
        '+f': lambda l, r: scope.fadd(l, r, "tmp"),
        '-f': lambda l, r: scope.fsub(l, r, "tmp"),
        '*f': lambda l, r: scope.fmul(l, r, "tmp"),
        '/f': lambda l, r: scope.fdiv(l, r, "tmp"),
        '%f': lambda l, r: scope.frem(l, r, "tmp"),
        '==b': lambda l, r: scope.icmp(ICMP_EQ, l, r, "tmp"),
        '&&b': lambda l, r: scope.and_(l, r, "tmp"),
        '||b': lambda l, r: scope.or_(l, r, "tmp")
        }
    return tmp[self.op](left[0], right[0]),left[1];

class UnaryOp(SyntaxNode):
  def __init__(self, op, expression):
    self.op = op
    self.expression = expression

  def codeGen(self, scope):
    pass

class Call(SyntaxNode):
  def __init__(self, name, arguments):
    self.name = name
    self.arguments = arguments

  def codeGen(self, scope):
    pass

