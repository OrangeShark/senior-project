from src import ast,tokenSpec

tokens = tokenSpec.tokens

precedence = (
     ('left', 'PLUS', 'MINUS'),
     ('left', 'TIMES', 'DIVIDE'),
     ('left', 'MOD'),
     ('left', 'EQ', 'NE', 'LE', 'LT', 'GT', 'GE'),
     ('left', 'OR', 'AND'),
     ('right', 'PIPE')
)

def p_program(t):
  'program : imports declaration_list'
  t[0] = ast.Program(t[1], t[2])

def p_empty(t):
  'empty :'
  pass

def p_imports(t):
  '''imports : imports_list
             | empty'''
  t[0] = t[1]

def p_imports_list(t):
  '''imports_list : imports_list import_declaration
                  | import_declaration'''
  if(len(t) == 2):
    t[0] = [t[1]]
  else:
    t[0] = t[1]
    t[0].append(t[2])

def p_import_declaration(t):
  'import_declaration : IMPORT ID SEMI'
  t[0] = ast.ImportDeclaration(t[2])

def p_declaration_list(t):
  '''declaration_list : declaration_list declaration
                      | declaration'''
  if(len(t) == 2):
    t[0] = [t[1]]
  else:
    t[0] = t[1]
    t[0].append(t[2])

def p_declaration(t):
  '''declaration : var_declaration
                 | function_declaration
                 | class_declaration'''
  t[0] = t[1]

def p_var_declaration(t):
  '''var_declaration : type ID SEMI
                     | type ID ASSIGN expression SEMI'''
  if len(t) == 4:
    t[0] = ast.VariableDeclaration(t[1], t[2])
  else:
    t[0] = ast.VariableDeclaration(t[1], t[2], t[4])

def p_function_declaration(t):
  'function_declaration : type ID LPAREN params RPAREN compound_stmt'
  t[0] = ast.Function(t[1], t[2], t[4], t[6])

def p_type(t):
  '''type : VOID
          | INT
          | FLOAT
          | STRING
          | BOOLEAN
          | CHAR'''
  t[0] = t[1]

def p_params(t):
  '''params : param_list
            | empty'''
  t[0] = t[1]

def p_param_list(t):
  '''param_list : param_list COMMA param
                | param'''
  if(len(t) == 2):
    t[0] = [t[1]]
  else:
    t[0] = t[1]
    t[0].append(t[3])

def p_pram(t):
  'param : type ID'
  t[0] = ast.Param(t[1], t[2])

def p_class_declaration(t):
  'class_declaration : CLASS ID class_block'
  t[0] = ast.ClassDeclaration(t[2], t[3])

def p_class_block(t):
  'class_block : empty'
  pass

def p_compound_stmt(t):
  'compound_stmt : LBRACE statement_list RBRACE'
  t[0] = t[2]

def p_statement_list(t):
  '''statement_list : statement_list statement
                    | statement'''
  if len(t) == 2:
    t[0] = [t[1]]
  else:
    t[0] = t[1]
    t[0].append(t[2])

def p_statement(t):
  '''statement : expression_stmt
               | compound_stmt
               | selection_stmt
               | iteration_stmt
               | return_stmt
               | var_declaration'''
  t[0] = t[1]

def p_expression_stmt(t):
  'expression_stmt : expression SEMI'
  t[0] = t[1]

def p_selection_stmt(t):
  '''selection_stmt : if_stmt
                    | if_else_stmt'''
  t[0] = t[1]

def p_if_stmt(t):
  'if_stmt : IF LPAREN expression RPAREN statement'
  t[0] = ast.IfStmt(t[3], t[5])

def p_if_else_stmt(t):
  'if_else_stmt : IF LPAREN expression RPAREN statement ELSE statement'
  t[0] = ast.IfElseStmt(t[3], t[5], t[7])

def p_iteration_stmt(t):
  '''iteration_stmt : while_stmt
                    | for_stmt'''
  t[0] = t[1]

def p_while_stmt(t):
  'while_stmt : WHILE LPAREN expression RPAREN statement'
  t[0] = ast.WhileStmt(t[3], t[5])

def p_for_stmt(t):
  'for_stmt : FOR LPAREN var_declaration SEMI expression SEMI assignment'
  pass

def p_return_stmt(t):
  '''return_stmt : RETURN SEMI
                 | RETURN expression SEMI'''
  length = len(t)
  if(length == 3):
    t[0] = ast.ReturnStmt()
  else:
    t[0] = ast.ReturnStmt(t[2])

def p_expression(t):
  '''expression : assignment
                | binary
                | unary
                | call
                | variable
                | literal
                | paren_expr
                | array'''
  t[0] = t[1]

def p_assignment(t):
  'assignment : variable ASSIGN expression'
  t[0] = ast.Assignment(t[1], t[3])


def p_variable(t):
  '''variable : ID
              | ID LBRACKET expression RBRACKET'''
  if len(t) == 2:
    t[0] = ast.Variable(t[1])
  else:
    t[0] = ast.Variable(t[1], t[3])

def p_literal(t):
  '''literal : integer
             | float
             | boolean 
             | string
             | character'''
  t[0] = t[1]

def p_integer(t):
  'integer : INTLIT'
  t[0] = ast.Integer(t[1])

def p_float(t):
  'float : FLOATLIT'
  t[0] = ast.Float(t[1])

def p_boolean(t):
  '''boolean : TRUE
             | FALSE'''
  t[0] = ast.Boolean(t[1])

def p_string(t):
  'string : STRLIT'
  t[0] = ast.String(t[1])

def p_character(t):
  'character : CHARLIT'
  t[0] = ast.Character(t[1])

def p_paren_expr(t):
  'paren_expr : LPAREN expression RPAREN'
  t[0] = t[2]

def p_binary(t):
  'binary : expression binary_op expression'
  t[0] = ast.BinaryOp(t[1],t[2], t[3])

def p_unary(t):
  'unary : unary_op expression'
  t[0] = ast.UnaryOp(t[1], t[2])

def p_binary_op(t):
  '''binary_op : PLUS
               | MINUS
               | TIMES
               | DIVIDE
               | MOD
               | LT
               | LE
               | GT
               | GE
               | EQ
               | NE
               | AND
               | OR'''
  t[0] = t[1]

def p_unary_op(t):
  '''unary_op : MINUS
              | NOT'''
  t[0] = t[1]

def p_call(t):
  'call : ID LPAREN arguments RPAREN'
  t[0] = ast.Call(t[1], t[3])

def p_arguments(t):
  '''arguments : argument_list
              | empty'''
  t[0] = t[1]

def p_argument_list(t):
  '''argument_list : argument_list COMMA expression
                   | expression'''
  if(len(t) == 2):
    t[0] = [t[1]]
  else:
    t[0] = t[1]
    t[0].append(t[3])

def p_array_literal(t):
  'array : LBRACE list RBRACE'
  t[0] = ast.Array(t[2])

def p_list(t):
  '''list : list element
          | empty'''
  if len(t) == 2:
    t[0] = []
  else:
    t[0] = t[1]
    t[0].append[2]

def p_element(t):
  'element : literal'
  t[0] = t[1]

def p_error(t):
  print("Syntax error " + t.value)

