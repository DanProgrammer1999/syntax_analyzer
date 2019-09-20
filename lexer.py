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
    delimiters = "()"
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
                elif curr in " \n\t":
                    return Token(token_type, res)
                else:
                    self.push_back(Token(self.__resolve_type(curr)))
                    return Token(token_type, res)
        else:
            return Token(token_type)

    @staticmethod
    def __resolve_type(token):
        if token in Lexer.operators:
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

        elif token in Lexer.delimiters:
            if token == "(":
                return TokenType.LeftParen
            if token == ")":
                return TokenType.RightParen
        elif token.isdigit():
            return TokenType.Literal
        elif token in " \n\t":
            return 0
        else:
            return -1


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
