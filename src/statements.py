from .expressions import Expr
from .helper import Token

class Stmt:
    def __init__(self):
        pass

class PrintStmt(Stmt):
    def __init__(self, expr:Expr):
        self.expr = expr

    def __repr__(self):
        return f"( PrintStmt {self.expr} )" 
    
class ExprStmt(Stmt):
    def __init__(self, expr:Expr):
        self.expr = expr

    def __repr__(self):
        return f"( ExprStmt {self.expr} )" 
    
class VarDeclStmt(Stmt):
    def __init__(self, name, initializer:Expr):
        self.name = name
        self.initializer = initializer

    def __repr__(self):
        return f"( VarDeclStmt {self.name} = {self.initializer} )" 
    
class BlockStmt(Stmt):
    def __init__(self, statments:list[Stmt]):
        self.statments = statments

    def __repr__(self):
        return f"( BlockStmts {self.statments} )" 
    
class IfStmt(Stmt):
    def __init__(self, condition:Expr, thenBranch:Stmt, elseBranch:Stmt):
        self.condition = condition
        self.thenBranch = thenBranch
        self.elseBranch = elseBranch

    def __repr__(self):
        return f"( IfStmt {self.condition} : {self.thenBranch} else {self.elseBranch} )" 
    
class WhileStmt(Stmt):
    def __init__(self, condition:Expr, thenBranch:Stmt, increment:Expr=None):
        self.condition = condition
        self.thenBranch = thenBranch
        self.increment = increment

    def __repr__(self):
        return f"( WhileStmt {self.condition} : {self.thenBranch})"  
    
class BreakStmt(Stmt):
    def __init__(self):
        pass

    def __repr__(self):
        return f"Break" 
    
class ContStmt(Stmt):
    def __init__(self):
        pass

    def __repr__(self):
        return f"Continue" 
    
class FunDeclStmt(Stmt):
    def __init__(self, name:Token, parameters:list[Token], body:BlockStmt):
        self.name = name
        self.parameters = parameters
        self.body = body

    def __repr__(self):
        return f"( FunDecl {self.name} {self.parameters} : {self.body} )" 
    
class ReturnStmt(Stmt):
    def __init__(self, keyword, value):
        self.keyword = keyword
        self.value= value

    def __repr__(self):
        return f"( Return {self.keyword} {self.value} )" 