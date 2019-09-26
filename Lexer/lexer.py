from Lexer.token_types import TokenType
from Exceptions.exceptions import IllegalCharacterException, InvalidNumberFormatException


class Token:
    """
    Contains the type and value of a token
    """
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
        """
        Get current line number and position
        :return: tuple with current line number and position
        """
        return self.line_number, self.line_position

    def push_back(self, token):
        """
        Push back the unused token
        :param token: the token to push back
        """
        self.__pushback.append(token)

        # Decrement the position
        self.line_position -= 1
        if self.line_position < 0:
            self.line_position = 0
            self.line_number -= 1

    def get(self):
        """
        Get the next token from the file
        :return: token with determined type and value
        """

        # First, check the pushback
        if self.__pushback:
            self.line_position += 1
            return self.__pushback.pop()

        # Get raw value
        token_type, value = self.__get_next()
        # End of file
        if not value:
            return None

        # Skip all whitespace characters
        while token_type is token_type.Space:
            token_type, value = self.__get_next()
            if not value:
                return None

        if token_type is TokenType.Literal:
            curr = ""
            # Collect all digits of the number
            while token_type is TokenType.Literal:
                curr += value
                token_type, value = self.__get_next()

            # Number literal which begins with 0 and has more than 1 digit is illegal
            if len(curr) > 1 and curr.startswith('0'):
                raise InvalidNumberFormatException(self.filename, (self.line_number, self.line_position - 1), curr)

            if token_type and token_type is not token_type.Space:
                # If the last symbol was followed by meaningful, put it in pushback
                self.push_back(Token(token_type, value))

            return Token(TokenType.Literal, curr)

        return Token(token_type, value)

    def __get_next(self):
        """
        Get next raw (not processed, only 1 character is read) token
        :return: tuple with (token_type, value) for the read character.
        """

        # EOF was reached and file was closed
        if self.__fd.closed:
            return None, None

        curr = self.__fd.read(1)
        # If EOF reached
        if not curr:
            self.__fd.close()
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
        """
        Determine type of the raw token
        :param token: the raw version of token (just 1 character)
        :return:      TokenType for the token
        """
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