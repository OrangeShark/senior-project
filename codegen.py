#!/usr/bin/env python3
import os
from llvm.ee import *

class Codegen:

  def __init__(self, ast):
    self.ast = ast
    
  def generateIR(self, moduleName):
    module = self.ast.codeGen(moduleName)    
    return(module)
    
  def generateBinary(self, moduleName):
    module = self.ast.codeGen(moduleName)
    return module.to_bitcode()