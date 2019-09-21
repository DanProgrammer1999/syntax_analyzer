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


class IllegalCharacterException(LexicalException):
    def __init__(self, filename=None, position=None, character=None):
        text = "illegal character"
        if character:
            text += ": \'{}\'".format(character)
        super().__init__(filename, position, text)


class InvalidNumberFormatException(LexicalException):
    def __init__(self, filename=None, position=None, number=None):
        text = "bad number format: number{}starts with 0".format(" {} ".format(number) if number else " ")
        super().__init__(filename, position, text)
