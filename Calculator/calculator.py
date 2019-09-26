from Parser.parser import Parser
from Lexer.token_types import TokenType


def calculate(filename):
    tree = Parser().parse(filename)
    return evaluate_tree(tree)


def evaluate_tree(tree):
    if not tree:
        return None

    if tree.type == TokenType.Literal:
        return tree.value

    res = __eval_function([evaluate_tree(child) for child in tree.children], tree.type)

    return res


def __eval_function(operands, operator):

    if operator == TokenType.OpPlus:
        return int(operands[0]) + int(operands[1])
    elif operator == TokenType.OpMinus:
        return int(operands[0]) - int(operands[1])
    elif operator == TokenType.OpMultiply:
        return int(operands[0]) * int(operands[1])
    elif operator == TokenType.OpEquals:
        return int(operands[0]) == int(operands[1])
    elif operator == TokenType.OpLessThan:
        return int(operands[0]) < int(operands[1])
    elif operator == TokenType.OpMoreThan:
        return int(operands[0]) > int(operands[1])
    else:
        raise Exception("Operator not recognized")
