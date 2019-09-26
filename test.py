try:
    import pptree
except ImportError:
    pptree = None
    print("To visualize ast tree, you can use module \'pptree\'.\nYou can use pip to install it\n\n")

from Parser.parser import Parser
from Calculator import calculator

filename = input("Input name of the file with the expression:\t")
tree = Parser().parse(filename)

if pptree and tree:
    pptree.print_tree(tree)

res = calculator.evaluate_tree(tree)
print("Result:", res)
