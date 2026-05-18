from .interpreter import Interpret
from .expressions import (
    Expr,
    Unary, 
    Binary, 
    Literal, 
    Grouping, 
    Variable, 
    Assignment,
    Logical,
    Call
)
from .statements import (
    Stmt, 
    ExprStmt, 
    PrintStmt, 
    VarDeclStmt,
    BlockStmt,
    IfStmt,
    WhileStmt,
    BreakStmt,
    ContStmt,
    FunDeclStmt,
    ReturnStmt
)
from .helper import Token
from functools import singledispatch

class Resolver(Expr, Stmt):
    def __init__(self, interpreter:Interpret):
        self.interpreter:Interpret = interpreter
        self.scopes:list[dict] = []
    
    @singledispatch
    def resolve(self, stmts):
        self.error(stmts, "wrong resolve type")

    @resolve.register(list)
    def _(self, stmts:list[Stmt]):
        for stmt in stmts:
            self.resolve(stmt)
    
    @resolve.register(Stmt)
    def _(self, stmt: Stmt):
        match stmt:
            case PrintStmt():
                self.resolve_printstmt(stmt)
            case ExprStmt():
                self.resolve_exprstmt(stmt)
            case VarDeclStmt():
                self.resolve_vardeclstmt(stmt)
            case BlockStmt():
                self.resolve_blockstmt(stmt)
            case FunDeclStmt():
                self.resolve_fundeclstmt(stmt)
            case IfStmt():
                self.resolve_ifstmt(stmt)
            case WhileStmt():
                self.resolve_whilestmt(stmt)
            case BreakStmt():
                self.resolve_breakstmt(stmt)
            case ContStmt():
                self.resolve_contstmt(stmt)
            case ReturnStmt():
                self.resolve_returnstmt(stmt)
            case _:
                self.error(stmt, "Invalid statement")

    @resolve.register(Expr)
    def _(self, expr:Expr):
        match expr:
            case Binary():
                return self.resolve_binary_expr(expr)
            case Unary():
                return self.resolve_unary_expr(expr)
            case Grouping():
                return self.resolve_grouping_expr(expr)  
            case Literal():
                return self.resolve_literal_expr(expr) 
            case Variable():
                return self.resolve_variable_expr(expr) 
            case Assignment():
                return self.resolve_assign_expr(expr)
            case Logical():
                return self.resolve_logical_expr(expr)
            case Call():
                return self.resolve_call_expr(expr)
            case _:
                return self.error(expr, "Unknown Type")
    
    def resolve_blockstmt(self, stmt:BlockStmt):
        self.begin_scope()
        self.resolve(stmt.statments)
        self.end_scope()
        return None
    
    def resolve_vardeclstmt(self, stmt:VarDeclStmt):
        self.declare(stmt.name)
        if stmt.initializer:
            self.resolve(stmt.initializer)

        self.define(stmt.name)
        return None
    
    def resolve_fundeclstmt(self, stmt:FunDeclStmt):
        self.begin_scope()
        for param in stmt.parameters:
            self.declare(param.value);
            self.define(param.value);
    
        self.end_scope()
        return None
    
    def resolve_exprstmt(self, stmt:ExprStmt):
        self.resolve(stmt.expr);
        return None
    
    def resolve_printstmt(self, stmt:PrintStmt):
        self.resolve(stmt.expr);
        return None
    
    def resolve_ifstmt(self, stmt:IfStmt):
        self.resolve(stmt.condition);
        self.resolve(stmt.thenBranch)
        if stmt.elseBranch:
            self.resolve(stmt.elseBranch)
        return None
    
    def resolve_whilestmt(self, stmt:WhileStmt):
        self.resolve(stmt.condition)
        self.resolve(stmt.thenBranch)
        return None
    
    def resolve_breakstmt(self, stmt:BreakStmt):
        return None
    
    def resolve_contstmt(self, stmt:ContStmt):
        return None
    
    def resolve_returnstmt(self, stmt:ReturnStmt):
        if stmt.value:
            self.resolve(stmt.value)
        return None
    
    def declare(self, name:str):
        if len(self.scopes) <= 0:
            return None
        self.scopes[-1][name] = False

    def define(self, name:str):
        if len(self.scopes) <= 0:
            return None
        self.scopes[-1][name] = True
    
    def begin_scope(self):
        self.scopes.append({})

    def end_scope(self):
        self.scopes.pop()


    """ 
    Expr evalutions
    """

    def resolve_variable_expr(self, expr:Variable):
        if len(self.scopes) != 0:
            if self.scopes[-1][expr.token.value] == False:
                self.error(expr, "No Variable to resolve ??")

        self._resolve_local_var(expr)
        return None

    def resolve_assign_expr(self, expr:Assignment):
        self.resolve(expr.value)    
        self._resolve_local_var(expr, expr.name)
        return None

    def resolve_binary_expr(self, expr:Binary):
        self.resolve(expr.left)
        self.resolve(expr.right) 
        return None   

    def resolve_call_expr(self, expr:Call):
        self.resolve(expr.callee)    
        for arg in expr.args:
            self.resolve(arg)
        return None

    def resolve_grouping_expr(self, expr:Grouping):
        self.resolve(expr.expr)    
        return None
    
    def resolve_literal_expr(self, expr:Literal):   
        return None
    
    def resolve_unary_expr(self, expr:Unary):  
        self.resolve(expr.right) 
        return None
    
    def resolve_logical_expr(self, expr:Logical):  
        self.resolve(expr.left) 
        self.resolve(expr.right) 
        return None
    
    def _resolve_local_var(self, expr:Variable, name:str):
        for index, scope in enumerate(reversed(self.scopes)):
            if scope.get(name, None):
                self.interpreter.resolve(expr, len(self.scopes) - index - 1)
                break
        return None
    

    