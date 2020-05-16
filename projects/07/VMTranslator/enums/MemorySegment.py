from enum import Enum


class MemorySegment(Enum):
    ARGUMENT = 'argument'
    LOCAL = 'local'
    STATIC = 'static'
    CONSTANT = 'constant'
    THIS = 'this'
    THAT = 'that'
    POINTER = 'pointer'
    TEMP = 'temp'
