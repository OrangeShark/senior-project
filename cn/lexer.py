import ply.lex as lex
from cn import tokenSpec

class Lexer:
  def __init__(self, log=lex.NullLogger(), **kwargs):
    self.build(log, **kwargs)

  def build(self, log, **kwargs):
    self.lexer = lex.lex(module=tokenSpec, errorlog=log, **kwargs)

  def scan(self, data):
    self.lexer.input(data)

  def token(self):
    return self.lexer.token()

