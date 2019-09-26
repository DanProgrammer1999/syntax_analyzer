try:
    import pptree
except ImportError:
    pptree = None
    print("To visualize ast tree, you can use module \'pptree\'.\n You can use pip to install it")

from syntax_parser import Parser
import calculator

filename = input("Input name of the file with the expression:\t")
tree = Parser().parse(filename)

if pptree:
    pptree.print_tree(tree)

res = calculator.evaluate_tree(tree)
print("Result:", res)
