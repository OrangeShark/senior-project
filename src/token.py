# Reserved words
reserved = {
    # control flow
    'if' : 'IF',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'for' : 'FOR',
    # primitive data types
    'int' : 'INT',
    'float' : 'FLOAT',
    'void' : 'VOID',
    'char' : 'CHAR',
    'string' : 'STRING',
    'boolean' : 'BOOLEAN',
    'true', : 'TRUE',
    'false', : 'FALSE',
    
    'var' : 'VAR',
    'func' : 'FUNC',
    'class' : 'CLASS',

    'return' : 'RETURN',
    'import' : 'IMPORT'
    }

tokens = (
  # Literals
  'ID',
  'INTLIT',
  'FLOATLIT',
  'STRLIT'
  'CHARLIT',

  # Operators
  'PLUS',
  'MINUS',
  'TIMES',
  'DIVIDE',
  'MOD', # Modulus
  'OR',
  'AND',
  'NOT',
  'LT', # < 
  'LE', # <=
  'GT', # >
  'GE', # >=
  'EQ', # ==
  'NE', # !=
  'PIPE' # |>

  # Increment and decrement
  'PLUSPLUS',
  'MINUSMINUS',

  # Assignment
  'ASSIGN',

  # Delimiters
  'LPAREN',
  'RPAREN',
  'LBRACKET',
  'RBRACKET',
  'LBRACE',
  'RBRACE',
  'COMMA',
  'SEMI'
  ) + list(reserved.values())


def t_newline(t):
  r'\n+'
  t.lexer.lineno += len(t.value)

t_ignore = ' \t'

# Operators
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MOD = r'%'
t_OR = r'\|\|'
t_AND = r'&&'
t_NOT = r'!'
t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='
t_EQ = r'=='
t_NE = r'!='
t_PIPE = r'\|>'

# Assignment
t_ASSIGN = r'='

# Increment and Decrement
t_PLUSPLUS = r'\+\+'
t_MINUSMINUS = r'--'

# Delimieters
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMMA = r','
t_SEMI = r';'

def t_ID(t):
  r'[a-zA-Z_][a-zA-Z_0-9]*'
  t.type = reserved.get(t.value, 'ID')
  return t

def t_INTLIT(t):
  r'\d+'
  t.value = int(t.value)
  return t

def t_FLOATLIT(t):
  r'\d+\.\d+'
  t.value = float(t.value)
  return t

def t_CHARLIT(t):
  r'\'\w\''
  t.value = t.value[1]
  return t

def t_STRLIT:
  r'\".*?\"'
  t.value = t.value[1:-1]
  return t

  

def t_error(t):
  print "Illegal character '%s'" % t.value[0]
  t.lexer.skip(1)


