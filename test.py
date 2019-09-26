# Try to import pptree module

from Parser.parser import Parser
from Calculator import calculator


def main():
    filename = input("Input name of the file with the expression:\t")
    tree = Parser().parse(filename)
    if not tree:
        print("File is empty")
        exit(0)

    try:
        import pptree
        pptree.print_tree(tree)
    except ImportError:
        print("You can use module \'pptree\' to visualize ast tree.\nUse pip to install it\n\n")

    res = calculator.evaluate_tree(tree)
    print("Result:", res)


if __name__ == "__main__":
    main()
