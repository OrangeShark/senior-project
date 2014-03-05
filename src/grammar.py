from src import ast

precedence = (
    ('left', 'PLUS', 'MINUS')
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'MOD'),
    ('left', 'EQ', 'NE', 'LE', 'LT', 'GT', 'GE'),
    ('left', 'OR', 'AND'),
    ('right', 'PIPE')
)

def_

