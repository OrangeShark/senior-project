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
  t[0] = Program(t[1], t[2])

def p_empty(t):
  'empty :'
  pass

def p_imports(t):
  '''imports : imports import_declaration
             | empty'''
  if(len(p) == 4):
    t[0] = Imports(t[1], t[2])

def p_import_declaration(t):
  'import_declaration : IMPORT ID SEMI'
  t[0] = ImportDeclaration(t[2])

def p_declaration_list(t):
  '''declaration_list : declaration-list declaration
                      | declaration'''

def p_declaration(t):
  '''declaration : var_declaration
                 | function_declaration
                 | class_declaration'''
  t[0] = t[1]

def p_var_declaration(t):
  'var_declaration : type_specifier ID SEMI'
  t[0] = VariableDeclaration(t[1], t[2])

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
  t[0] = t[1]
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
  t[0] = ClassDeclaration(t[2], t[3])

def p_compound_stmt(t):
  'compound_stmt : LBRACE statement_list RBRACE'
  t[0] = t[2]

def p_statement_list(t):
  '''statement_list : statement_list statement
                    | empty'''

def p_statement(t):
  '''statement : expression_stmt
               | compound_stmt
               | selection_stmt
               | iteration_stmt
               | return_stmt'''
  t[0] = t[1]

def p_expression_stmt(t):
  'expression_stmt : expression SEMI'
  t[0] = t[1]

def p_selection_stmt(t):
  '''selection_stmt : if_stmt
                    | if_else_stmt'''

def p_if_stmt(t):
  'if_stmt : IF LPAREN expression RPAREN statement'
  t[0] = IfStmt(t[3], t[5])

def p_if_else_stmt(t):
  'if_else_stmt : if_stmt ELSE statement'
  t[0] = IfElseStmt(t[1], t[3])

def p_iteration_stmt(t):
  '''iteration_stmt : while_stmt'''
  t[0] = t[1]

def p_while_stmt(t):
  'while_stmt : WHILE LPAREN expression RPAREN statement'
  t[0] = WhileStmt(t[3], t[5])

def p_return_stmt(t):
  '''return_stmt : RETURN SEMI
                 | RETURN expression SEMI'''
  lenth = len(t)
  if(length == 3):
    t[0] = ReturnStmt()
  else:
    t[0] = ReturnStmt(t[2])

def p_expression_stmt(t):
  'expression_stmt : expression SEMI'
  t[0] = t[1]

def p_expression(t):
  '''expression : assignment
                | binary
                | unary
                | call
                | variable
                | literal
                | paren_expr'''
  t[0] = t[1]

def p_assignment(t):
  'assignment : variable ASSIGN expression'
  t[0] = Assignment(t[1], t[3])

def p_variable(t):
  'variable : ID'
  t[0] = t[1]

def p_binary(t):
  'binary: expression binary_op expression'
  t[0] = BinaryOp(t[1],t[2], t[3])

def p_unary(t):
  'unary: unary_op expression'
  t[0] = UnaryOp(t[1], t[2])

def binary_op(t):
  '''binary_op : PLUS
               | MINUS
               | TIMES
               | DIVIDE'''
  t[0] = t[1]

def unary_op(t):
  '''unary_op : MINUS'''
  t[0] = t[1]
