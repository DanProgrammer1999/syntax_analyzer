from lexer import Lexer
from token_types import TokenType


class AstNode:
    def __init__(self, token):
        self.__token = token
        self.parent = None
        self.children = None


class Parser:
    def __init__(self, filename):
        self.filename = filename
        self.__lexer = Lexer(self.filename)
        self.tree = self.__construct_tree()

    def __construct_tree(self):
        return self.__parse_expression()

    def __parse_expression(self):
        return self.__parse_expression()

    def __parse_relation(self):
        left = self.__parse_term()
        parent = self.__lexer.get()
        if not parent:
            return left

        expected_types = (TokenType.Operator.Equals, TokenType.Operator.LessThan, TokenType.Operator.MoreThan)

        if parent.type not in expected_types:
            raise UnexpectedTokenException(self.filename, "expected either of these symbols: \'>\', \'<\', or \'=\'")

        right = self.__parse_term()

        return self.__make_binary_tree(AstNode(parent), left, right)

    def __parse_term(self):
        left = self.__parse_factor()

        while True:
            parent = self.__lexer.get()

            if not parent:
                return left

            expected_types = (TokenType.Operator.Plus, TokenType.Operator.Minus)
            if parent.type not in expected_types:
                raise UnexpectedTokenException(self.filename,
                                               "expected either of these symbols: \'+\', or \'-\', got {}".format(
                                                   parent.type))

            right = self.__parse_factor()

            left = self.__make_binary_tree(AstNode(parent), left, right)

        return left

    def __parse_factor(self):

        left = self.__parse_primary()
        while True:
            parent = self.__lexer.get()
            if not parent:
                return left

            if parent.type is not TokenType.Operator.Multiply:
                # TODO implement
                # self.__lexer.push_back(left)
                print("Not implemented yet")
                exit(-1)

    def __parse_primary(self):
        left = self.__lexer.get()
        if left.type is TokenType.Delimiter.LeftParen:
            left = self.__parse_expression()

            if self.__lexer.get().type is not TokenType.Delimiter.RightParen:
                raise UnexpectedTokenException(self.filename, "missing closing parenthesis")

        elif left.type is not TokenType.Literal:
            raise UnexpectedTokenException(self.filename, "malformed expression: expected integer or parenthesis")

        return AstNode(left)

    @staticmethod
    def __make_binary_tree(parent: AstNode, child1: AstNode, child2: AstNode):
        assert not parent.children
        parent.children = [child1, child2]
        child1.parent, child2.parent = parent, parent
        return parent


class Error(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class UnexpectedTokenException(Error):
    def __init__(self, filename=None, text=None):
        self.value = "Unexpected token exception"
        if filename:
            self.value += " in file {}".format(filename)

        if text:
            self.value += ": {}".format(text)
