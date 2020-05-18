from enum import Enum


class Arithmetic(Enum):
    ADD = 'add'
    SUB = 'sub'
    EQ = 'eq'
    GT = 'gt'
    LT = 'lt'
    AND = 'and'
    OR = 'or'
    NEG = 'neg'
    NOT = 'not'


class Command(Enum):
    C_ARITHMETIC = 'C_ARITHMETIC'
    C_PUSH = 'C_PUSH'
    C_POP = 'C_POP'
    C_LABEL = 'C_LABEL'
    C_GOTO = 'C_GOTO'
    C_IF = 'C_IF'
    C_FUNCTION = 'C_FUNCTION'
    C_RETURN = 'C_RETURN'
    C_CALL = 'C_CALL'


class MemorySegment(Enum):
    ARGUMENT = 'argument'
    LOCAL = 'local'
    STATIC = 'static'
    CONSTANT = 'constant'
    THIS = 'this'
    THAT = 'that'
    POINTER = 'pointer'
    TEMP = 'temp'
