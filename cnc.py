#!/usr/bin/env python3
from cn import lexer, parser, codegen
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
  c = codegen.Codegen(p.parse(s.scan(source)))
  
  if(args.verbose):
    print(c.generateIR(moduleName))
  else:
    fileName = moduleName + ".bc"
    output = open(fileName, 'w+b')
    output.write(c.generateBinary(moduleName))

if __name__ == '__main__':
  main()

