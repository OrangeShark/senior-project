#!/usr/bin/env python3
from cn import lexer, parser
import argparse
import os
from llvm.ee import *

def main():
  argp = argparse.ArgumentParser(description='A compiler for the C natural language')
  argp.add_argument('infile', help='source file')
  argp.add_argument('-v', '--verbose', action='store_true')
  args = argp.parse_args()
  
  moduleName = args.infile.split('.')[0]

  s = lexer.Lexer()
  p = parser.Parser()

  source = open(args.infile).read()
  ast = p.parse(s.scan(source))
  
  module = ast.codeGen(moduleName)
  fileName = moduleName + ".bc"
  output = open(fileName, 'w+b')
  if(args.verbose):
    print(module)
  module.to_bitcode(output)

if __name__ == '__main__':
  main()

