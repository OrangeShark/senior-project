import ply.yacc as yacc
from src import grammar

class Parser:
  def __init__(self):
    self.build()

  def build(self, **kwargs):
    self.parser = yacc.yacc(module=grammar, **kwargs)

  def parse(lexer):
    #TODO finish parse
    pass
