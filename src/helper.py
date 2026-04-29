import re
from dataclasses import dataclass
from enum import Enum, auto

class TokenType(Enum):
    # Comments
    MULTILINE_COMMENT = auto()
    COMMENT = auto()

    # Single char
    WHITESPACE = auto()
    OPEN_PAR = auto()
    CLOSE_PAR = auto()
    OPEN_BRACE = auto()
    CLOSE_BRACE = auto()
    SEMICOLON = auto()
    COMMA = auto()
    SLASH = auto()
    STAR = auto()
    DOT = auto()
    MINUS = auto()
    PLUS = auto()

    # One or two char
    BANG_EQUAL = auto()
    EQUAL_EQUAL = auto()
    GREATER_EQUAL = auto()
    LESS_EQUAL = auto()
    BANG = auto()
    EQUAL = auto()
    GREATER = auto()
    LESS = auto()

    # Keywords
    AND = auto()
    CLASS = auto()
    ELSE = auto()
    FALSE = auto()
    FUN = auto()
    FOR = auto()
    IF = auto()
    NIL = auto()
    OR = auto()
    PRINT = auto()
    RETURN = auto()
    SUPER = auto()
    THIS = auto()
    TRUE = auto()
    VAR = auto()
    WHILE = auto()
    BREAK = auto()
    CONTINUE = auto()

    # Literals
    STRING = auto()
    IDENTIFIER = auto()
    CONSTANT = auto()

    # Special
    EOF = auto()

@dataclass
class TokenPattern:
    type: TokenType
    regex: re.Pattern
    string: str

    def __init__(self, type:TokenType, pattern:str, string:str=None):
        self.type = type
        self.regex = re.compile(pattern)
        self.string = string

@dataclass
class Token:
    type: TokenType # token type
    value: str # the raw text that was matched
    line: int
    column: int
    #the interpreted value, distinct from raw text

    def __init__(self, type:TokenType, value, line:int=0, column=0):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"{self.type.name}:{self.type.value} {self.value} at {self.line}:{self.column}\n"

KEYWORDS = {
    "and": TokenType.AND,
    "class": TokenType.CLASS,
    "else": TokenType.ELSE,
    "false": TokenType.FALSE,
    "fun": TokenType.FUN,
    "for": TokenType.FOR,
    "if": TokenType.IF,
    "nil": TokenType.NIL,
    "or": TokenType.OR,
    "print": TokenType.PRINT,
    "return": TokenType.RETURN,
    "super": TokenType.SUPER,
    "this": TokenType.THIS,
    "true": TokenType.TRUE,
    "var": TokenType.VAR,
    "while": TokenType.WHILE,
    "break": TokenType.BREAK,
    "continue": TokenType.CONTINUE,
}