from src import lexer, parser
import argparse
import os
from llvm.ee import *

def main():
  argp = argparse.ArgumentParser(description='A compiler for the C natural language')
  argp.add_argument('infile', help='source file')
  args = argp.parse_args()

  s = lexer.Lexer()
  p = parser.Parser()

  source = open(args.infile).read()
  ast = p.parse(s.scan(source))
  
  module = ast.codeGen("test")
  fileName = args.infile.split('.')[0] + ".bc"
  output = open(fileName, 'w+b')
  print(module)
  module.to_bitcode(output)

if __name__ == '__main__':
  main()

