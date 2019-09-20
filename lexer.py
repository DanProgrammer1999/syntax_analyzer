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
        self.__tokens = self.__scan(filename)
        self.position = 0

    def get(self):
        value = self.__tokens[self.position]
        self.position += 1
        return value

    @staticmethod
    def __scan(filename):
        res = []
        buffer = ""
        line_number = 0
        line_position = 0
        with open(filename, 'r') as fd:

            while True:
                curr = fd.read(1)
                line_position += 1
                if not curr:
                    if buffer != "":
                        res.append(Token(TokenType.Literal, buffer))
                    break

                if curr == ' ':
                    if buffer != "":
                        res.append(Token(TokenType.Literal, buffer))
                        buffer = ""
                    continue

                if curr in Lexer.operators:
                    if buffer != "":
                        res.append(Token(TokenType.Literal, buffer))
                        buffer = ""

                    if curr == "+":
                        res.append(Token(TokenType.Operator.Plus))
                    if curr == "-":
                        res.append(Token(TokenType.Operator.Minus))
                    if curr == "*":
                        res.append(Token(TokenType.Operator.Multiply))
                    if curr == "<":
                        res.append(Token(TokenType.Operator.LessThan))
                    if curr == ">":
                        res.append(Token(TokenType.Operator.MoreThan))
                    if curr == "=":
                        res.append(Token(TokenType.Operator.Equals))

                elif curr in Lexer.delimiters:
                    if buffer != "":
                        res.append(Token(TokenType.Literal, buffer))
                        buffer = ""

                    if curr == ";":
                        res.append(Token(TokenType.Delimiter.Semicolon))
                    if curr == "(":
                        res.append(Token(TokenType.Delimiter.LeftParen))
                    if curr == ")":
                        res.append(Token(TokenType.Delimiter.RightParen))
                    if curr == "\n":
                        line_number += 1
                        line_position = 0
                        res.append(Token(TokenType.Delimiter.NewLine))
                elif curr.isdigit():
                    if buffer == "0":
                        raise LexicalException(filename, (line_number, line_position - 1),
                                               "illegal integer literal: cannot start with \'0\'")

                    buffer += curr
                else:
                    raise LexicalException(filename, (line_number, line_position),
                                           "illegal symbol \'{}\': not a token".format(curr))
        return res


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