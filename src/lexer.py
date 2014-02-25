import ply.lex as lex
import token

class Lexer:
  def __init__(self):
    self.build()

  def build(self, **kwargs):
    self.lexer = lex.lex(module=token, **kwargs)

  def scan(self, data):
    self.lexer.input(data)

  def token(self):
    return self.lexer.token()
