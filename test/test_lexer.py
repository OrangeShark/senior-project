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
      self.assertEqual(token.value, int(int_lit))
 
  float_tokens = [
      "0.1",
      "3.14",
      ".9634523"
      ]
  def test_float_literal(self):
    for float_lit in self.float_tokens:
      self.scanner.scan(float_lit)
      token = self.scanner.token()
      self.assertEqual(token.type, "FLOATLIT")
      self.assertEqual(token.value, float(float_lit))
  
  string_tokens = [
      '""',
      '"Hello World!"',
      '" \\" "'
      ]
  def test_string_literal(self):
    for string_lit in self.string_tokens:
      self.scanner.scan(string_lit)
      token = self.scanner.token()
      self.assertEqual(token.type, "STRLIT")
      self.assertEqual(token.value, string_lit[1:-1])
  
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


