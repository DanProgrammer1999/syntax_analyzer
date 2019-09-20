from enum import Enum


class OperatorType(Enum):
    Equals = 0
    LessThan = 1
    MoreThan = 2
    Minus = 3
    Plus = 4
    Multiply = 5


class DelimiterType(Enum):
    LeftParen = 0
    RightParen = 1
    Semicolon = 2
    NewLine = 3


class Token(Enum):
    Operator = OperatorType
    Delimiter = DelimiterType
    Literal = 0