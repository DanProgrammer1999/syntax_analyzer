# Intro

This is a simple parser for mathematical expressions with operators `[+, -, *, <, >, =]`, and support for parentheses, 
as per task description.

# Structure
### TokenType
It is a simple class which describes all possible token types for this expression language

### Lexer

#### Usage
Although you can use it independently from `Parser`, you cannot manually pass an instance of `Lexer` to it.
To use it, pass filename to initializer: `l = Lexer('file.m')` . To get next token, use `l.get()`. To put token back, 
use `l.push_back(token)`. Next time you invoke `get()` method, it will return that exact token.   

#### Details
Lexer class is designed in the following way: 
 - It contains class `Token`, which keeps type and value of a token
 - When method `get()` is invoked, it reads next symbol from the file, and decides on what to do next: 
    - continue to read and concatenate symbols, if this symbol is a digit
    - skip and get next symbol, if this symbol is a whitespace character
    - return the Token instance
    - return None, if the lexer reached end of file
 - It has method `push_back(token)` which allows parser to put the unused token on stack. 
 When `get()` is invoked, it checks the `push_back` buffer and returns items from there, if it is not empty. 
 - Lexer keeps track of current line number and position for better exception reports.


### Parser
#### Usage

To parse the file and build an AST tree, use `parse` method: `tree = Parser().parse('filename')`. 
The filename can also be specified in `Parser` object initialization: `p = Parser('filename')`, and then `tree = p.parse()`
So, you can reuse the same instance of `Parser` for different files.

#### Details
It simply has one function for each item in the given grammar rules. 
Interesting and useful observations:
- Useful note: you can use [pptree](https://github.com/clemtoy/pptree) to display the tree.
- `AstNode` class represents a simple tree node with variable number of children. It stores `Token` instance 
(and allows read-only access to its type and value), parent and list of children.
- Error handling: it is not very obvious at which point an error should be handled (in other words, at which rule). 
I had to debug program for some extreme cases (for example, empty file) to uncover some bugs in error handling.

### Calculator
#### Usage
It has several functions that you can use to evaluate the expression:
- `evaluate_tree(tree)` accepts `AstNode`, root of the tree to be traversed, and evaluates it. 
If the tree is `None`, returns `None`
- `calculate(filename)` accepts filename, uses `Parser` to build AST tree, and then calls `evaluate_tree(tree)` 
to evaluate the tree.

#### Details
First of all, let us look at `__eval_function(operands, operator)`. This function is used to calculate the result 
of operator over operands. It works really simple: depending on operator, it executes the corresponding operation over 
operands and returns the result.


`evaluate_tree(tree)` works recursively: if the node is a literal, it just returns its value. Otherwise, returns 
the result of `eval_function(operands, operator)`, where operands are the results of recursive call for all of 
the children of the current node, and operator is the value of this node: 

```python
    res = __eval_function([evaluate_tree(child) for child in tree.children], tree.type)
```

### Error Handling 

There are several types of errors for lexer and for parser, all of which inherit from `SyntaxError` and invoke its 
constructor with filename and position, and optionally custom text.

For lexer, there are 2 types of exceptions: 
- `IllegalCharacterException` for an unknown character
- `InvalidNumberFormatException` for a malformed number (i.e. `007`, `00`, etc.)

For parser, there are 3 types of exceptions:
- `UnexpectedTokenException` for a misplaced token (i.e. `1 ++`, `2 *=`, `(2 + 3) )`, etc.)
- `UnexpectedEOF` for a situation when a token was expected, but was not provided (i.e. `1 +`, `2 *`, `(2 + ` etc.)
- `MissingParenthesisException` for a missing closing parenthesis (i.e. `(2 + 3` )

