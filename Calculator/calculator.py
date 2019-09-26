from Parser.parser import Parser
from Lexer.token_types import TokenType


def calculate(filename):
    """
    Calculate an expression from a file
    :param filename: name of file containing the expression
    :return:         result of evaluating the expression in the file. None, if the file was empty
    """
    tree = Parser().parse(filename)
    return evaluate_tree(tree)


def evaluate_tree(tree):
    """
    Evaluate the AST tree starting with node tree
    :param tree: root node of an AST tree to be evaluated
    :return:     result of tree evaluation. None, if the root was None; an integer, otherwise
    """

    if not tree:
        return None

    # If this node is a leaf node
    if tree.type == TokenType.Literal:
        return tree.value

    # Otherwise, use operator on the children, recursively
    # In case of binary tree (in our case it's always either binary or one-leafed):
    # evaluate left child, evaluate right child, use the operator on the resulting operands
    res = __eval_function([evaluate_tree(child) for child in tree.children], tree.type)

    return res


def __eval_function(operands, operator):
    """
    Apply the operator to operands
    :param operands: list of operands with the length of arity of the operator
    :param operator: the operator to be applied to operands
    :return:         the result of application of the operator to the operands
    """

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
