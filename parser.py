from lexer import Lexer
from token_types import TokenType


class AstNode:
    def __init__(self, token):
        self.__token = token
        self.parent = None
        self.children = None

    def __repr__(self):
        s = str(self.__token.type)
        if self.__token.type is TokenType.Literal:
            s += ": {}".format(self.__token.value)

        return s

class Parser:
    def __init__(self, filename):
        self.filename = filename
        self.__lexer = Lexer(self.filename)
        self.tree = self.__construct_tree()

    def __construct_tree(self):
        return self.__parse_expression()

    def __parse_expression(self):
        return self.__parse_relation()

    def __parse_relation(self):
        left = self.__parse_term()
        parent = self.__lexer.get()
        if not parent:
            return left

        expected_types = (TokenType.OpEquals, TokenType.OpLessThan, TokenType.OpMoreThan)

        if parent.type not in expected_types:
            self.__lexer.push_back(parent)
            return left
            # raise UnexpectedTokenException(self.filename, "expected either of these symbols: \'>\', \'<\', or \'=\'")

        right = self.__parse_term()

        return self.__make_binary_tree(AstNode(parent), left, right)

    def __parse_term(self):
        left = self.__parse_factor()
        parent = self.__lexer.get()

        while parent:

            expected_types = (TokenType.OpPlus, TokenType.OpMinus)
            if parent.type not in expected_types:
                self.__lexer.push_back(parent)
                break

            right = self.__parse_factor()
            left = self.__make_binary_tree(AstNode(parent), left, right)
            parent = self.__lexer.get()

        return left

    def __parse_factor(self):

        left = self.__parse_primary()
        parent = self.__lexer.get()
        while parent:

            if parent.type is not TokenType.OpMultiply:
                self.__lexer.push_back(parent)
                break

            right = self.__parse_primary()
            left = self.__make_binary_tree(AstNode(parent), left, right)
            parent = self.__lexer.get()

        return left

    def __parse_primary(self):
        left = self.__lexer.get()
        if left.type is TokenType.LeftParen:
            left = self.__parse_expression()

            if self.__lexer.get().type is not TokenType.RightParen:
                raise UnexpectedTokenException(self.filename, "missing closing parenthesis")
            return left

        elif left.type is not TokenType.Literal:
            raise UnexpectedTokenException(self.filename, "malformed expression: expected integer or parenthesis")
        return AstNode(left)

    @staticmethod
    def __make_binary_tree(parent: AstNode, child1: AstNode, child2: AstNode):
        assert not parent.children
        parent.children = [child1, child2]
        child1.parent, child2.parent = parent, parent
        return parent

    def __repr__(self):
        curr_nodes = [self.tree]
        res = ""
        while curr_nodes:
            new_nodes = []
            for node in curr_nodes:
                res += "{" + str(node) + "}\t"

                if node.children:
                    new_nodes += node.children
            res += "\n"
            curr_nodes = new_nodes

        return res

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
