import ply.yacc as yacc
from src import grammar

class Parser:
  def __init__(self, **kwargs):
    self.build(**kwargs)

  def build(self, **kwargs):
    self.parser = yacc.yacc(module=grammar, **kwargs)

  def parse(self, lexer):
    return self.parser.parse(lexer=lexer)
