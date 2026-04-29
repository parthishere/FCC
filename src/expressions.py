from .helper import TokenType, Token

"""
expression = exp.Binary(
                exp.Unary(TokenType.MINUS, exp.Literal(123)),
                TokenType.STAR,
                exp.Grouping(exp.Literal(45.67))
            )

print(expression)
"""

class Expr:
    def __init__(self):
        pass

class Binary(Expr):
    def __init__(self, left:Expr, operator:Token, right:Expr):
        self.left = left
        self.right = right
        self.operator = operator
    
    def __repr__(self):
        return f"( {self.operator.value} {self.left} {self.right} )"

class Unary(Expr):
    def __init__(self, operator:Token, right:Expr):
        self.right = right
        self.operator = operator

    def __repr__(self):
        return f"( {self.operator.value} {self.right} )"
    
class Logical(Expr):
    def __init__(self, left:Expr, operator:Token, right:Expr):
        self.left = left
        self.operator = operator
        self.right = right
    
    def __repr__(self):
        return f"( {self.operator.value} {self.left} {self.right} )"

class Literal(Expr):
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return f"{self.value}"

class Grouping(Expr):
    def __init__(self, expr:Expr):
        self.expr = expr
    
    def __repr__(self):
        return f"( Group {self.expr} )"

class Identifier(Expr):
    def __init__(self, token:Token):
        self.token = token

    def __repr__(self):
        return f"( Var {self.token.value} )"

class Assignment(Expr):
    def __init__(self, name:str, value):
        self.name = name
        self.value = value
    
    def __repr__(self):
        return f"( VarAssign {self.name} = {self.value} )"
    