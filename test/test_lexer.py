import unittest
from src import lexer

class TestLexerTokens(unittest.TestCase):
  def setUp(self):
    self.scanner = lexer.Lexer()

  def test_int_literal(self):
    # check for integer literals
    self.scanner.scan("2")
    token = self.scanner.token()
    self.assertEqual(token.type, "INTLIT")
    self.scanner.scan("0")
    token = self.scanner.token()
    self.assertEqual(token.type, "INTLIT")
    self.scanner.scan("12")
    token = self.scanner.token()
    self.assertEqual(token.type, "INTLIT")
    self.scanner.scan("1234")
    token = self.scanner.token()
    self.assertEqual(token.type, "INTLIT")

