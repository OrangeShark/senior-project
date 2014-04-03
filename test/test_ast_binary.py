#!/usr/bin/env python

# Import the llvmpy modules.
import unittest
from cn import ast
from llvm import *
from llvm.core import *
from llvm.ee import *

class FakeLexToken(object):
  def __init__(self, type, value):
    self.type = type
    self.value = value

class Mock(object):
    def __init__(self, **kwds):
        self.__dict__.update(kwds)
    
class FakeNode(object):
  def __init__(self, codegen):
    self.codegen = codegen
  def codeGen(self, scope):
    return self.codegen

class TestAST(unittest.TestCase):

  def test_binaryop_sunny1(self):
    my_module = Module.new('my_module')
    ty_int = Type.int()     # by default 32 bits
    ty_func = Type.function(ty_int, [])
    f_sum = my_module.add_function(ty_func, "main")
    bb = f_sum.append_basic_block("entry")
    builder = Builder.new(bb)
    left = FakeNode((builder.add(Constant.int(ty_int, 5), Constant.int(ty_int, 0), "tmp"),'INT'))
    right = FakeNode((builder.add(Constant.int(ty_int, 5), Constant.int(ty_int, 0), "tmp"),'INT'))
    binaryNode = ast.BinaryOp(left, '+', right)
    tmp = binaryNode.codeGen(builder)
    builder.ret(tmp[0])
    ee = ExecutionEngine.new(my_module)
    retval = ee.run_function(f_sum, [])
    self.assertEqual(retval.as_int_signed(), 10)
    self.assertEqual('INT', tmp[1])
    
  def test_binaryop_sunny2(self):
    my_module = Module.new('my_module')
    ty_int = Type.int()     # by default 32 bits
    ty_func = Type.function(ty_int, [])
    f_sum = my_module.add_function(ty_func, "main")
    bb = f_sum.append_basic_block("entry")
    builder = Builder.new(bb)
    left = FakeNode((builder.add(Constant.int(ty_int, 5), Constant.int(ty_int, 0), "tmp"),'INT'))
    right = FakeNode((builder.add(Constant.int(ty_int, 7), Constant.int(ty_int, 0), "tmp"),'INT'))
    binaryNode = ast.BinaryOp(left, '-', right)
    tmp = binaryNode.codeGen(builder)
    builder.ret(tmp[0])
    ee = ExecutionEngine.new(my_module)
    retval = ee.run_function(f_sum, [])
    self.assertEqual(retval.as_int_signed(), -2)
    self.assertEqual('INT', tmp[1])

  def test_binaryop_rainy(self):
    my_module = Module.new('my_module')
    ty_int = Type.int()     # by default 32 bits
    ty_func = Type.function(ty_int, [])
    f_sum = my_module.add_function(ty_func, "main")
    bb = f_sum.append_basic_block("entry")
    builder = Builder.new(bb)
    left = FakeNode((builder.add(Constant.int(ty_int, -5), Constant.int(ty_int, 0), "tmp"),'INT'))
    right = FakeNode((builder.add(Constant.int(ty_int, 2), Constant.int(ty_int, 0), "tmp"),'INT'))
    binaryNode = ast.BinaryOp(left, '%', right)
    tmp = binaryNode.codeGen(builder)
    builder.ret(tmp[0])
    ee = ExecutionEngine.new(my_module)
    retval = ee.run_function(f_sum, [])
    self.assertEqual(retval.as_int_signed(), -1)
    self.assertEqual('INT', tmp[1])
