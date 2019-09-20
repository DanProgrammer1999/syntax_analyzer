from lexer import Lexer
from token_types import TokenType


class AstNode:
    def __init__(self, token_type, literal_value=None):
        self.__token_type = token_type
        if literal_value:
            self.__value = literal_value

        self.parent = None
        self.children = []


class Parser:
    def __init__(self, filename):
        self.filename = filename
        self.lexer = Lexer(filename)
