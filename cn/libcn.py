from llvm import *
from llvm.core import *

char = Type.int(8)
char_p = Type.pointer(char)

class LibCN():
  printf = Type.function(Type.int(32), [char_p], True)
  getchar = Type.function(Type.int(32), [])
  system = Type.function(Type.int(32), [char_p])
  scanf = Type.function(Type.int(32), [char_p], True)