import ply.yacc as yacc
from cn import grammar

class Parser:
  def __init__(self, log=yacc.NullLogger(), **kwargs):
    self.build(log, **kwargs)

  def build(self, log, **kwargs):
    self.parser = yacc.yacc(module=grammar, errorlog=log, **kwargs)

  def parse(self, lexer):
    return self.parser.parse(lexer=lexer)
