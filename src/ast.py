from abc import ABCMeta, abstractmethod
from llvm import *
from llvm.core import *

llvmTypes = {
    'INT', Type.int()
    }

class SyntaxNode(object):
  __metaclass__ = ABCMeta

  @abstractmethod
  def codeGen(self):
    pass

class Program(SyntaxNode):
  def __init__(self, imports, declarations):
    self.imports = imports
    self.declarations = declarations

  def codeGen(self):
    pass

class ImportDeclaration(SyntaxNode):
  def __init__(self, importID):
    self.importID = importID

  def codeGen(self):
    pass

class VariableDeclaration(SyntaxNode):
  def __init__(self, typeSpec, name):
    self.type = typeSpec
    self.name = name
 
  def codeGen(self):
    pass

class Function(SyntaxNode):
  def __init__(self, typeSpec, name, params, body):
    self.type = typeSpec
    self.name = name
    self.params = params
    self.body = body

  def codeGen(self, scope):
    params = [param.codeGen() for param in self.params]
    funcType = Type.function(llvmType[self.type], params)
    
    func = scope.module.add_function(funcType, self.name)
    
    for i, param in enumerate(self.params):
      func.args[i].name = param.name

    bb = func.append_basic_block("entry")
    scope.builder = Builder.new(bb)
      
    self.body.codeGen(scope)
    

class Param(SyntaxNode):
  def __init__(self, typeSpec, name):
    self.type = typeSpec
    self.name = name

  def codeGen(self, scope):
    return llvmType[self.type]   

class ClassDeclaration(SyntaxNode):
  def __init__(self, name, body):
    self.type = 'class'
    self.name = name
    self.body = body

  def codeGen(self):
    pass

class IfStmt(SyntaxNode):
  def __init__(self, condition, statement):
    self.condition = condition
    self.statement = statement

  def codeGen(self):
    pass

class IfElseStmt(SyntaxNode):
  def __init__(self, condition, statement1, statement2):
    self.condition = condition
    self.statement1 = statement1
    self.statement2 = statement2

  def codeGen(self):
    pass

class WhileStmt(SyntaxNode):
  def __init__(self, condition, statement):
    self.condition = condition
    self.statement = statement

  def codeGen(self):
    pass

class ReturnStmt(SyntaxNode):
  def __init__(self, expression):
    self.expression = expression

  def codeGen(self):
    pass

class Assignment(SyntaxNode):
  def __init__(self, variable, expression):
    self.variable = variable
    self.expression = expression

  def codeGen(self):
    pass

types = {
    'INTLIT' : 'int',
    'FLOATLIT' : 'float',
    'TRUE' : 'boolean',
    'FALSE' : 'boolean',
    'STRLIT' : 'string',
    'CHARLIT' : 'char'
    }

class Literal(SyntaxNode):
  def __init__(self, token):
    self.value = token.value
    self.type = types[token.type]

  def codeGen(self):
    ty = Type.int()
    val = Constant.int(ty, self.value)
    tmp = scope.add(val, Constant.int(ty, 0), "tmp")
    return tmp

class BinaryOp(SyntaxNode):
  def __init__(self, left, op, right):
    self.type = "binop"
    self.left = left
    self.right = right
    self.op = op

  def codeGen(self):
    pass

class UnaryOp(SyntaxNode):
  def __init__(self, op, expression):
    self.op = op
    self.expression = expression

  def codeGen(self):
    left = self.left.codeGen(scope)
    right = self.right.codeGen(scope)
    zero = Constant.int(Type.int(), 0)
    assert(type(left) == type(right))
    tmp = {'+': left.add(right),
        '-': left.sub(right),
        '*': left.mul(right),
        '/': left.sdiv(right),
        '%': left.srem(right)}
    return scope.add(tmp[self.op], zero, "tmp")

class Call(SyntaxNode):
  def __init__(self, name, arguments):
    self.name = name
    self.arguments

  def codeGen(self):
    pass
