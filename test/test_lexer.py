import unittest
from src import lexer

class TestLexerTokens(unittest.TestCase):
  def setUp(self):
    self.scanner = lexer.Lexer()

  def test_int_literal(self):
    # check for integer literals
    self.scanner.scan("0")
    token = self.scanner.token()
    self.assertEqual(token.type, "INTLIT")
    self.scanner.scan("1")
    token = self.scanner.token()
    self.assertEqual(token.type, "INTLIT")
    self.scanner.scan("2")
    token = self.scanner.token()
    self.assertEqual(token.type, "INTLIT")
    self.scanner.scan("3")
    token = self.scanner.token()
    self.assertEqual(token.type, "INTLIT")
    self.scanner.scan("4")
    token = self.scanner.token()
    self.assertEqual(token.type, "INTLIT")
    self.scanner.scan("5")
    token = self.scanner.token()
    self.assertEqual(token.type, "INTLIT")
    self.scanner.scan("6")
    token = self.scanner.token()
    self.assertEqual(token.type, "INTLIT")
    self.scanner.scan("7")
    token = self.scanner.token()
    self.assertEqual(token.type, "INTLIT")
    self.scanner.scan("8")
    token = self.scanner.token()
    self.assertEqual(token.type, "INTLIT")
    self.scanner.scan("9")
    token = self.scanner.token()
    self.assertEqual(token.type, "INTLIT")
    self.scanner.scan("10")
    token = self.scanner.token()
    self.assertEqual(token.type, "INTLIT")
    self.scanner.scan("12")
    token = self.scanner.token()
    self.assertEqual(token.type, "INTLIT")
    self.scanner.scan("1234")
    token = self.scanner.token()
    self.assertEqual(token.type, "INTLIT")

  def test_float_literal(self):
    self.scanner.scan("0.1")
    token = self.scanner.token()
    self.assertEqual(token.type, "FLOATLIT")
    self.scanner.scan("3.14")
    token = self.scanner.token()
    self.assertEqual(token.type, "FLOATLIT")



