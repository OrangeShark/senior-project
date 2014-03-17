from abc import ABCMeta, abstractmethod

class SyntaxNode(object):
  __metaclass__ = ABCMeta

  @abstractmethod
  def codeGen(self):
    pass

class Program(SyntaxNode):
  def __init__(self, imports, declarations):
    self.imports = imports
    self.declarations = declarions

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

  def codeGen(self):
    pass

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
    pass

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
    pass

class Call(SyntaxNode):
  def __init__(self, name, arguments):
    self.name = name
    self.arguments

  def codeGen(self):
    pass
