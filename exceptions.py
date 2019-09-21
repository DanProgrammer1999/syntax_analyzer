class Error(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class SyntaxError(Error):
    def __init__(self, filename, position, text=None):
        self.value = "Syntax error in file {} at position <{}:{}>".format(filename, position[0], position[1])
        if text:
            self.value += ": {}".format(text)

        self.value += "."


class UnexpectedTokenException(SyntaxError):
    def __init__(self, filename, position, token):
        super().__init__(filename, position, "unexpected token: {}".format(token))


class UnexpectedEOF(SyntaxError):
    def __init__(self, filename, position):
        super().__init__(filename, position, "reached end of file while parsing")


class MissingParenthesisException(SyntaxError):
    def __init__(self, filename, position):
        super().__init__(filename, position)


class IllegalCharacterException(SyntaxError):
    def __init__(self, filename=None, position=None, character=None):
        text = "illegal character"
        if character:
            text += ": \'{}\'".format(character)
        super().__init__(filename, position, text)


class InvalidNumberFormatException(SyntaxError):
    def __init__(self, filename=None, position=None, number=None):
        text = "bad number format: number{}starts with 0".format(" {} ".format(number) if number else " ")
        super().__init__(filename, position, text)
