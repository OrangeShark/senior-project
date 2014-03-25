from src import lexer, parser
import argparse
import os

def main():
  argp = argparse.ArgumentParser(description='A compiler for the C natural language')
  argp.add_argument('infile', help='source file')
  args = argp.parse_args()

  s = lexer.Lexer()
  p = parser.Parser()

  source = open(args.infile).read()
  ast = p.parse(s.scan(source))
  
  module = ast.codeGen("test")

  print(module)
  


if __name__ == '__main__':
  main()

