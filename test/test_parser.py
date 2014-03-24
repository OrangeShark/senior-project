import unittest
from src import parser, ast

class Lexer():
  def __init__(self, tokens):
    tokens.reverse()
    self.tokens = tokens

  def token(self):
    if(len(self.tokens) == 0):
        return None
    return self.tokens.pop()

class Token():
  def __init__(self, t, value=None):
    self.type = t
    if value == None:
      self.value = t
    else:
      self.value = value

class TestParserGrammar(unittest.TestCase):
  p = parser.Parser()

  functionDeclaration = [ Token("VOID"),
                          Token("ID", "main"),
                          Token("LPAREN"),
                          Token("RPAREN"),
                          Token("LBRACE"),
                          Token("ID", "print"),
                          Token("LPAREN"),
                          Token("RPAREN"),
                          Token("SEMI"),
                          Token("RBRACE")]
  def testFunctionDeclaration(self):
    l = Lexer(self.functionDeclaration)
    root = self.p.parse(l)
    self.assertIsInstance(root, ast.Program)
    self.assertEqual(len(root.declarations), 1)
    self.assertIsInstance(root.declarations[0], ast.Function)
    self.assertEqual(root.declarations[0].name, "main")
    self.assertEqual(root.declarations[0].typeSpec, "VOID")
  
  importDeclaration = [ Token("IMPORT"),
                        Token("ID", "lib"),
                        Token("SEMI"),
                        Token("VOID"),
                        Token("ID", "main"),
                        Token("LPAREN"),
                        Token("RPAREN"),
                        Token("LBRACE"),
                        Token("ID", "print"),
                        Token("LPAREN"),
                        Token("RPAREN"),
                        Token("SEMI"),
                        Token("RBRACE")]

  def testImportDeclaration(self):
    l = Lexer(self.importDeclaration)
    root = self.p.parse(l)
    self.assertIsInstance(root, ast.Program)
    self.assertEqual(len(root.imports), 1)
    self.assertIsInstance(root.imports[0], ast.ImportDeclaration)
    self.assertEqual(root.imports[0].name, "lib")

  variableDeclaration = [ Token("INT"),
                          Token("ID", "foo"),
                          Token("ASSIGN"),
                          Token("INTLIT", "2"),
                          Token("SEMI") ]
  def testVariableDeclaration(self):
    l = Lexer(self.variableDeclaration)
    root = self.p.parse(l)
    self.assertIsInstance(root, ast.Program)
    self.assertEqual(len(root.declarations), 1)
    self.assertIsInstance(root.declarations[0], ast.VariableDeclaration)

  functionParam = [ Token("VOID"),
                    Token("ID", "main"),
                    Token("LPAREN"),
                    Token("INT"),
                    Token("ID", "bar"),
                    Token("RPAREN"),
                    Token("LBRACE"),
                    Token("ID", "print"),
                    Token("LPAREN"),
                    Token("RPAREN"),
                    Token("SEMI"),
                    Token("RBRACE")]
  def testFunctionParam(self):
    l = Lexer(self.functionParam)
    root = self.p.parse(l)
    self.assertIsInstance(root, ast.Program)
    self.assertEqual(len(root.declarations), 1)
    self.assertIsInstance(root.declarations[0], ast.Function)
    func = root.declarations[0]
    self.assertEqual(len(func.params), 1)
    self.assertIsInstance(func.params[0], ast.Param)
    self.assertEqual(func.params[0].type, "INT")
    self.assertEqual(func.params[0].name, "bar")

  functionParams = [ Token("VOID"),
                    Token("ID", "main"),
                    Token("LPAREN"),
                    Token("INT"),
                    Token("ID", "bar"),
                    Token("COMMA"),
                    Token("FLOAT"),
                    Token("ID", "foo"),
                    Token("RPAREN"),
                    Token("LBRACE"),
                    Token("ID", "print"),
                    Token("LPAREN"),
                    Token("RPAREN"),
                    Token("SEMI"),
                    Token("RBRACE")]

  def testFunctionParams(self):
    l = Lexer(self.functionParams)
    root = self.p.parse(l)
    self.assertIsInstance(root, ast.Program)
    self.assertEqual(len(root.declarations), 1)
    self.assertIsInstance(root.declarations[0], ast.Function)
    func = root.declarations[0]
    self.assertEqual(len(func.params), 2)
    self.assertIsInstance(func.params[0], ast.Param)
    self.assertEqual(func.params[0].type, "INT")
    self.assertEqual(func.params[0].name, "bar")
    self.assertIsInstance(func.params[1], ast.Param)
    self.assertEqual(func.params[1].type, "FLOAT")
    self.assertEqual(func.params[1].name, "foo")
