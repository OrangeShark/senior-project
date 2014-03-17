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

