from cn import ast,tokenSpec

tokens = tokenSpec.tokens

precedence = (
     ('left', 'OR', 'AND'),
     ('left', 'EQ', 'NE', 'LE', 'LT', 'GT', 'GE'),
     ('left', 'PLUS', 'MINUS'),
     ('left', 'TIMES', 'DIVIDE'),
     ('left', 'MOD'),
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
    t[0] = ast.GVariableDeclaration(t[1], t[2])
  else:
    t[0] = ast.GVariableDeclaration(t[1], t[2], t[4])

def p_function_declaration(t):
  'function_declaration : type ID LPAREN params RPAREN compound_stmt'
  t[0] = ast.Function(t[1], t[2], t[4], t[6])

def p_type(t):
  '''type : VOID
          | INT
          | FLOAT
          | STRING
          | BOOLEAN
          | CHAR
          | ID
          | type LBRACKET RBRACKET'''
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
  'class_declaration : CLASS ID LBRACE class_block RBRACE'
  t[0] = ast.ClassDeclaration(t[2], t[4])

def p_class_block(t):
  'class_block : attribute_list constructor method_list'
  t[0] = (t[1], t[2], t[3])

def p_attribute_list(t):
  '''attribute_list : attribute_list attribute_declaration
                    | empty'''
  if len(t) == 2:
    t[0] = []
  else:
    t[0] = t[1]
    t[0].append(t[2])

def p_attribute(t):
  '''attribute_declaration : type ID SEMI
                           | type ID ASSIGN expression SEMI'''
  if len(t) == 4:
    t[0] = ast.ClassAttribute(t[1], t[2])
  else:
    t[0] = ast.ClassAttribute(t[1], t[2], t[4])

def p_method_list(t):
  '''method_list : method_list method_declaration
                 | empty'''
  if len(t) == 2:
    t[0] = []
  else:
    t[0] = t[1]
    t[0].append(t[2])

def p_method_declaration(t):
  'method_declaration : type ID LPAREN params RPAREN compound_stmt'
  t[0] = ast.ClassMethod(t[1], t[2], t[4], t[6])

def p_constructor(t):
  'constructor : CONSTR LPAREN params RPAREN compound_stmt'
  t[0] = ast.ClassConstructor(t[3], t[5])

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
               | var_dec_stmt
               | array_dec_stmt'''
  t[0] = t[1]

def p_var_dec_stmt(t):
  '''var_dec_stmt : type ID SEMI
                  | type ID ASSIGN expression SEMI'''
  if len(t) == 4:
    t[0] = ast.VariableDeclaration(t[1], t[2])
  else:
    t[0] = ast.VariableDeclaration(t[1], t[2], t[4])

def p_array_dec_stmt(t):
  '''array_dec_stmt : type ID LBRACKET INTLIT RBRACKET SEMI
                    | type ID LBRACKET INTLIT RBRACKET array SEMI'''
  if len(t) == 7:
    t[0] = ast.ArrayDeclaration(t[1], t[2], t[4])
  else:
    t[0] = ast.ArrayDeclaration(t[1], t[2], t[4], t[6])

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
                | array
                | attribute_assign
                | class_attribute
                | method_call'''
  t[0] = t[1]

def p_attribute_assign(t):
  'attribute_assign : expression DOT ID ASSIGN expression'
  t[0] = ast.AttributeAssignment(t[1], t[3], t[5])

def p_class_attribute(t):
  'class_attribute : expression DOT ID'
  t[0] = ast.Attribute(t[1], t[3])

def p_method_call(t):
  'method_call : expression DOT ID LPAREN arguments RPAREN'
  t[0] = ast.MethodCall(t[1], t[3], t[5])

def p_assignment(t):
  '''assignment : ID ASSIGN expression
                | ID LBRACKET expression RBRACKET ASSIGN expression'''
  if len(t) == 4:
    t[0] = ast.Assignment(t[1], t[3])
  else:
    t[0] = ast.Assignment(t[1], t[6], t[3])


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
  '''binary : expression PLUS expression
            | expression MINUS expression
            | expression TIMES expression 
            | expression DIVIDE expression
            | expression MOD expression
            | expression LT expression
            | expression LE expression
            | expression GT expression
            | expression GE expression
            | expression EQ expression
            | expression NE expression
            | expression AND expression
            | expression OR expression'''
  t[0] = ast.BinaryOp(t[1],t[2], t[3])

def p_unary(t):
  'unary : unary_op expression'
  t[0] = ast.UnaryOp(t[1], t[2])

def p_unary_op(t):
  '''unary_op : MINUS
              | NOT'''
  t[0] = t[1]

def p_call(t):
  'call : expression LPAREN arguments RPAREN'
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

