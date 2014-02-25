import ply.lex as lex
from src import tokenSpec

class Lexer:
  def __init__(self):
    self.build()

  def build(self, **kwargs):
    self.lexer = lex.lex(module=tokenSpec, **kwargs)

  def scan(self, data):
    self.lexer.input(data)

  def token(self):
    return self.lexer.token()

