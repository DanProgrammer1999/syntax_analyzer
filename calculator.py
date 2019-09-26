from syntax_parser import Parser, AstNode
from token_types import TokenType


def calculate(filename):
    tree = Parser().parse(filename)
    return evaluate_tree(tree)


def evaluate_tree(tree: AstNode):
    if not tree:
        return None

    if tree.type == TokenType.Literal:
        return tree.value

    res = eval_function([evaluate_tree(child) for child in tree.children], tree.type)

    return res


def eval_function(literals, operator):

    if operator == TokenType.OpPlus:
        return int(literals[0]) + int(literals[1])
    elif operator == TokenType.OpMinus:
        return int(literals[0]) - int(literals[1])
    elif operator == TokenType.OpMultiply:
        return int(literals[0]) * int(literals[1])
    elif operator == TokenType.OpEquals:
        return int(literals[0]) == int(literals[1])
    elif operator == TokenType.OpLessThan:
        return int(literals[0]) < int(literals[1])
    elif operator == TokenType.OpMoreThan:
        return int(literals[0]) > int(literals[1])
    else:
        raise Exception("Operator not recognized")
