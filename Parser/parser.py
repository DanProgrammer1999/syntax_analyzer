from Lexer.lexer import Lexer
from Lexer.token_types import TokenType
from Exceptions.exceptions import UnexpectedTokenException, MissingParenthesisException, UnexpectedEOF


class AstNode:
    def __init__(self, token):
        self.__token = token
        self.parent = None
        self.children = []

        # For pptree lib
        self.name = self.__repr__()

    @property
    def type(self):
        return self.__token.type

    @property
    def value(self):
        return self.__token.value

    def __repr__(self):
        s = str(self.__token.type)
        if self.__token.type is TokenType.Literal:
            s += ": {}".format(self.__token.value)

        return s


class Parser:
    def __init__(self, filename=None):
        self.filename = filename
        if filename:
            self.__lexer = Lexer(filename)

    def parse(self, filename=None):
        """
        Parse the expression in file specified by filename
        Filename can be specified on initialization, as well
        :param filename: The filename from which the expression should be parsed
        :return:         The root of the built tree
        """
        if filename:
            self.filename = filename
            self.__lexer = Lexer(filename)

        if not self.filename:
            print("No filename provided!")
            return None

        return self.__construct_tree()

    def __construct_tree(self):
        res = self.__parse_expression()
        t = self.__lexer.get()
        # Expression is parsed, but EOF is not reached -> something extra in the file
        if t:
            raise UnexpectedTokenException(self.filename, self.__lexer.get_position(), t.value)

        return res

    def __parse_expression(self):
        """
        expression -> relation
        """
        return self.__parse_relation()

    def __parse_relation(self):
        """
        relation -> term [ ( "<" | ">" | "=" ) term ]
        """
        left = self.__parse_term()
        parent = self.__lexer.get()
        if not parent:
            return left

        expected_types = (TokenType.OpEquals, TokenType.OpLessThan, TokenType.OpMoreThan)

        # Could be ")"
        if parent.type not in expected_types:
            self.__lexer.push_back(parent)
            return left

        right = self.__parse_term()
        if not right:
            raise UnexpectedEOF(self.filename, self.__lexer.get_position())

        return self.__make_binary_tree(AstNode(parent), left, right)

    def __parse_term(self):
        """
        term -> factor { ( "+" | "-" ) factor }
        """
        left = self.__parse_factor()
        parent = self.__lexer.get()

        while parent:

            expected_types = (TokenType.OpPlus, TokenType.OpMinus)
            if parent.type not in expected_types:
                self.__lexer.push_back(parent)
                break

            right = self.__parse_factor()
            if not right:
                raise UnexpectedEOF(self.filename, self.__lexer.get_position())

            left = self.__make_binary_tree(AstNode(parent), left, right)
            parent = self.__lexer.get()

        return left

    def __parse_factor(self):
        """
        factor -> primary { "*" primary }
        """
        left = self.__parse_primary()
        parent = self.__lexer.get()
        while parent:

            if parent.type is not TokenType.OpMultiply:
                self.__lexer.push_back(parent)
                break

            right = self.__parse_primary()
            if not right:
                raise UnexpectedEOF(self.filename, self.__lexer.get_position())

            left = self.__make_binary_tree(AstNode(parent), left, right)
            parent = self.__lexer.get()

        return left

    def __parse_primary(self):
        """
        primary -> integer | "(" expression ")"
        """
        left = self.__lexer.get()
        if left is None:
            # Could be an empty file
            return left

        if left.type is TokenType.LeftParen:
            left = self.__parse_expression()

            closing_paren = self.__lexer.get()
            if not closing_paren or closing_paren.type is not TokenType.RightParen:
                raise MissingParenthesisException(self.filename, self.__lexer.get_position())
            return left
        elif left.type is TokenType.Literal:
            return AstNode(left)
        else:
            raise UnexpectedTokenException(self.filename, self.__lexer.get_position(), left.value)

    @staticmethod
    def __make_binary_tree(parent: AstNode, child1: AstNode, child2: AstNode):
        """
        Create a tree stump with two children
        :param parent: parent node
        :param child1: first child node
        :param child2: second child node
        :return:       root node (parent node) with specified children
        """
        parent.children = [child1, child2]
        child1.parent, child2.parent = parent, parent
        return parent
