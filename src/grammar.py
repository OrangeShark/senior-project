from src import ast

precedence = (
    ('left', 'PLUS', 'MINUS')
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'MOD'),
    ('left', 'EQ', 'NE', 'LE', 'LT', 'GT', 'GE'),
    ('left', 'OR', 'AND'),
    ('right', 'PIPE')
)

def p_program(t):
  'program : imports declaration_list'

def p_empty(t):
  'empty :'
  pass

def p_imports(t):
  '''imports : imports import_declaration
           | empty'''

def p_import_declaration(t):
  'import_declaration : IMPORT ID SEMI'

def p_declaration_list(t):
  '''declaration_list : declaration-list declaration
                      | declaration'''

def p_declaration(t):
  '''declaration : var_declaration
                 | function_declaration
                 | class declaration'''

def p_var_declaration(t):
  'var_declaration : type_specifier ID SEMI'
  #t[0] = TODO Some AST node

def p_function_declaration(t):
  'function_declaration : type_specifier ID LPAREN params RPAREN compound_stmt'
  #t[0] = TODO

def p_type_specifier(t):
  '''type : VOID
          | INT
          | FLOAT
          | STRING
          | BOOLEAN
          '''
  #t[0] = TODO
def p_params(t):
  '''params : param_list
            | empty'''

def p_param_list(t):
  '''param_list : param_list COMMA param
                | param'''
  #t[0] = TODO

def p_pram(t):
  'param : type_specifier ID'

def p_class_declaration(t):
  'class_declaration : CLASS ID class_block'
  #t[0] = TODO

def p_compound_stmt(t):
  'compound_stmt : LBRACE statement_list RBRACE'

def p_statement_list(t):
  '''statement_list : statement_list statement
                    | empty'''

def p_statement(t):
  '''statement : expression_stmt
               | compound_stmt
               | selection_stmt
               | iteration_stmt
               | return_stmt'''

def p_expression_stmt(t):
  'expression_stmt : expression SEMI'

def p_selection_stmt(t):
  '''selection_stmt : if_stmt
                    | if_else_stmt'''

def p_if_stmt(t):
  'if_stmt : IF LPAREN expression RPAREN statement'

def p_if_else_stmt(t):
  'if_else_stmt : if_stmt ELSE statement'

def p_iteration_stmt(t):
  '''iteration_stmt : while_stmt'''

def p_while_stmt(t):
  'while_stmt : WHILE LPAREN expression RPAREN statement'

def p_return_stmt(t):
  '''return_stmt : RETURN SEMI
                 | RETURN expression SEMI'''

