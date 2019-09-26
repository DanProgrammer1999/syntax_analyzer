from token_types import TokenType
from exceptions import IllegalCharacterException, InvalidNumberFormatException


class Token:
    def __init__(self, token_type, literal_value=None):
        self.type = token_type
        self.value = literal_value

    def __repr__(self):
        if self.type == TokenType.Literal:
            return "{}: {}".format("Literal", self.value)
        else:
            return str(self.type)


class Lexer:

    def __init__(self, filename):
        self.filename = filename
        self.line_number = 1
        self.line_position = 0

        self.__fd = open(filename, 'r')
        self.__pushback = []

    def get_position(self):
        return self.line_number, self.line_position

    def push_back(self, token):
        self.__pushback.append(token)
        self.line_position -= 1
        if self.line_position < 0:
            self.line_position = 0
            self.line_number -= 1

    def get(self):

        if self.__pushback:
            return self.__pushback.pop()

        token_type, value = self.__get_next()
        if not value:
            return None

        while token_type is token_type.Space:
            token_type, value = self.__get_next()
            if not value:
                return None

        if token_type is TokenType.Literal:
            curr = ""
            while token_type is TokenType.Literal:
                curr += value
                token_type, value = self.__get_next()

            if len(curr) > 1 and curr.startswith('0'):
                raise InvalidNumberFormatException(self.filename, (self.line_number, self.line_position), curr)
            if not token_type or token_type is token_type.Space:
                return Token(TokenType.Literal, curr)
            else:
                self.push_back(Token(token_type, value))
                return Token(TokenType.Literal, curr)

        return Token(token_type, value)

    def __get_next(self):
        curr = self.__fd.read(1)
        if not curr:
            return None, None
        token_type = self.__resolve_type(curr)
        if token_type is TokenType.Unknown:
            raise IllegalCharacterException(self.filename, (self.line_number, self.line_position), curr)
        if curr == "\n":
            self.line_number += 1
            self.line_position = 0
        else:
            self.line_position += 1

        return token_type, curr

    @staticmethod
    def __resolve_type(token):
        if token == "+":
            return TokenType.OpPlus
        if token == "-":
            return TokenType.OpMinus
        if token == "*":
            return TokenType.OpMultiply
        if token == "<":
            return TokenType.OpLessThan
        if token == ">":
            return TokenType.OpMoreThan
        if token == "=":
            return TokenType.OpEquals
        if token == "(":
            return TokenType.LeftParen
        if token == ")":
            return TokenType.RightParen
        if token.isdigit():
            return TokenType.Literal
        if token in " \n\t":
            return TokenType.Space

        return TokenType.Unknown