from token_types import TokenType


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
    delimiters = "\n;()"
    operators = "*+-<>="

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
        self.line_position += 1
        if not curr:
            return None

        if curr == ' ':
            return self.get()

        if curr == '\n':
            self.line_position = 0
            self.line_number += 1
            return self.get()

        if curr in Lexer.operators:
            res = None
            if curr == "+":
                res = Token(TokenType.OpPlus)
            if curr == "-":
                res = Token(TokenType.OpMinus)
            if curr == "*":
                res = Token(TokenType.OpMultiply)
            if curr == "<":
                res = Token(TokenType.OpLessThan)
            if curr == ">":
                res = Token(TokenType.OpMoreThan)
            if curr == "=":
                res = Token(TokenType.OpEquals)

        elif curr in Lexer.delimiters:
            if curr == "(":
                return Token(TokenType.LeftParen)
            if curr == ")":
                return Token(TokenType.RightParen)

        elif curr.isdigit():
            res = curr
            while True:
                curr = self.get()
                if curr.isdigit():
                    res += curr
                else:
                    self.push_back(curr)
                    return curr
        else:
            raise LexicalException(self.filename, (self.line_number, self.line_position),
                                   "illegal symbol \'{}\': not a token".format(curr))


class Error(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class LexicalException(Error):
    def __init__(self, filename=None, position: tuple = None, custom_text=None):
        text = "Lexical Exception"
        if filename:
            text += " in {}".format(filename)
        if position:
            text += " at line {}, position {}".format(position[0], position[1])
        if custom_text:
            text += ": {}".format(custom_text)
        text += '.'
        self.value = text
