from enum import Enum


class Token(Enum):
    KEYWORD = 'keyword'
    SYMBOL = 'symbol'
    IDENTIFIER = 'identifier'
    INT_CONST = 'int_const'
    STRING_CONST = 'string_const'


class Keyword(Enum):
    CLASS = 'class'
    METHOD = 'method'
    FUNCTION = 'function'
    CONSTRUCTOR = 'constructor'
    INT = 'int'
    BOOLEAN = 'boolean'
    CHAR = 'char'
    VOID = 'void'
    VAR = 'var'
    STATIC = 'static'
    FIELD = 'field'
    LET = 'let'
    DO = 'do'
    IF = 'if'
    ELSE = 'else'
    WHILE = 'while'
    RETURN = 'return'
    TRUE = 'true'
    FALSE = 'false'
    NULL = 'null'
    THIS = 'this'


class Symbol(Enum):
    LEFT_CURLY_BRACKET = '{'
    RIGHT_CURLY_BRACKET = '}'
    LEFT_ROUND_BRACKET = '('
    RIGHT_ROUND_BRACKET = ')'
    LEFT_SQUARE_BRACKET = '['
    RIGHT_SQUARE_BRACKET = ']'
    PERIOD = '.'
    COMMA = ','
    SEMI_COLON = ';'
    PLUS_SIGN = '+'
    HYPHEN = '-'
    ASTERISK = '*'
    SLASH = '/'
    AMPERSAND = '&'
    VERTICAL_LINE = '|'
    LESS_THAN_SIGN = '<'
    GREATER_THAN_SIGN = '>'
    EQUAL = '='
    TILDE = '~'
