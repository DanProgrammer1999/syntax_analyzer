from token_types import TokenType
from exceptions import LexicalException

class Token:
    def __init__(self, token_type, literal_value=None):
        self.type = token_type
        if token_type == TokenType.Literal:
            assert literal_value is not None
            self.value = literal_value

    def __repr__(self):
        if self.type == TokenType.Literal:
            return "{}: {}".format("Literal", self.value)
        else:
            return str(self.type)


class Lexer:

    def __init__(self, filename):
        self.filename = filename
        self.line_number = 0
        self.line_position = 0

        self.__fd = open(filename, 'r')
        self.__pushback = []

    def push_back(self, token):
        self.__pushback.append(token)

    def get(self):

        if self.__pushback:
            return self.__pushback.pop()

        curr = self.__fd.read(1)
        if not curr:
            return None

        token_type = self.__resolve_type(curr)
        if token_type == -1:
            raise LexicalException(self.filename, (self.line_number, self.line_position),
                                   "illegal character: \'{}\'".format(curr))
        elif token_type == 0:
            return self.get()
        elif token_type is TokenType.Literal:
            res = curr
            while True:
                curr = self.__fd.read(1)
                if curr is None:
                    return Token(token_type, curr)
                elif curr.isdigit():
                    res += curr
                else:
                    # If the current char is meaningful
                    if curr not in " \n\t":
                        self.push_back(Token(self.__resolve_type(curr)))
                    return Token(token_type, res)
        else:
            return Token(token_type)

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
            return 0

        return -1