import enum

class TokenType (enum.Enum):
    Operator = 0

    
class OperatorType (enum.Enum):
    Equals = 0

t = TokenType.Operator
print(t)

