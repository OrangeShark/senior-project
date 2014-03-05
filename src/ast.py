from abc import ABCMeta, abstractmethod

class SyntaxNode(object):
  __metaclass__ = ABCMeta

  @abstractmethod
  def codeGen(self):
    pass


class BinOp(SytaxNode):
  def __init__(self, left, op, right):
    self.type = "binop"
    self.left = left
    self.right = right
    self.op = op

  def codeGen(self):
    pass

