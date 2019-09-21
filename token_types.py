from enum import Enum, auto


class TokenType(Enum):
    Literal = auto()
    LeftParen = auto()
    RightParen = auto()

    OpEquals = auto()
    OpLessThan = auto()
    OpMoreThan = auto()
    OpMinus = auto()
    OpPlus = auto()
    OpMultiply = auto()

    Unknown = auto()
    Space = auto()
