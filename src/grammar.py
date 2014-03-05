from src import ast

precedence = (
    ('left', 'PLUS', 'MINUS')
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'MOD'),
    ('left', 'EQ', 'NE', 'LE', 'LT', 'GT', 'GE'),
    ('left', 'OR', 'AND'),
    ('right', 'PIPE')
)

def p_var_declaration(t):
  'var_declaration : type ID'
  #t[0] = TODO Some AST node

def p_function_declaration(t):
  'function_declaration : type ID param_list block'
  #t[0] = TODO

def p_type(t):
  '''type : VOID
          | INT
          | FLOAT
          | STRING
          | BOOLEAN
          '''
  #t[0] = TODO

def p_param_list(t):
  '''param_list : var_declaration COMMA param_list
                | var_declaration
                '''
  #t[0] = TODO

def p_class_declaration(t):
  'class_declaration : CLASS ID block'
  #t[0] = TODO
