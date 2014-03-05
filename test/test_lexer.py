import unittest
from src import lexer

class TestLexerTokens(unittest.TestCase):
  def setUp(self):
    self.scanner = lexer.Lexer()
  
  int_tokens = [
      "0",
      "1",
      "2",
      "3",
      "4",
      "5",
      "6",
      "7",
      "8",
      "9",
      "10",
      "123",
      "953246754"
      ]
  def test_int_literal(self):
    # check for integer literals
    for int_lit in self.int_tokens:
      self.scanner.scan(int_lit)
      token = self.scanner.token()
      self.assertEqual(token.type, "INTLIT")

  def test_float_literal(self):
    self.scanner.scan("0.1")
    token = self.scanner.token()
    self.assertEqual(token.type, "FLOATLIT")
    self.scanner.scan("3.14")
    token = self.scanner.token()
    self.assertEqual(token.type, "FLOATLIT")
    self.scanner.scan(".9634523")
    token = self.scanner.token()
    self.assertEqual(token.type, "FLOATLIT")

  
  def test_string_literal(self):
    self.scanner.scan('""')
    token = self.scanner.token()
    self.assertEqual(token.type, "STRLIT")
    self.assertEqual(token.value, "")
    self.scanner.scan('"Hello World!"')
    token = self.scanner.token()
    self.assertEqual(token.type, "STRLIT")
    self.assertEqual(token.value, "Hello World!")
  
  identifiers = [
      "foo",
      "_foo",
      "Foo",
      "Foo8",
      "FOO_BAR"
      ]

  def test_id(self):
    for identifier in self.identifiers:
      self.scanner.scan(identifier)
      token = self.scanner.token()
      self.assertEqual(token.type, "ID")


