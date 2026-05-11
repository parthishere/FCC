from .expressions import (
    Expr,
    Unary, 
    Binary, 
    Literal, 
    Grouping, 
    Identifier, 
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
from .helper import Token, TokenType
from .environment import Environment
from .callable import FCCallable, FCFunction
from .inbuilts import (
    ClockMS,
    ClockUS,
    ClockNS
)


class breakException(Exception):
    """Exception raised for break encounter."""
    pass

class contException(Exception):
    """Exception raised for continue encounter."""
    pass

class returnException(Exception):
    """Exception raised for continue encounter."""
    pass

class Interpret:
    
    def __init__(self, statements:list[Stmt], source:str="", filepath:str=""):
        self.statements = statements
        self.source = source
        self.filepath = filepath
        self.global_env = Environment()
        
        #defining clock class as inbuilt function
        self.global_env.define(ClockMS.name, ClockMS())
        self.global_env.define(ClockUS.name, ClockUS())
        self.global_env.define(ClockNS.name, ClockNS())

        self.environment = self.global_env
        self.has_error = False

    def interpret(self) -> None:
        statement = None

        for statement in self.statements:
            self.execute(statement)
            if self.has_error:
                return
        
    def execute(self, stmt: PrintStmt | ExprStmt | VarDeclStmt | BlockStmt | IfStmt | WhileStmt | FunDeclStmt):
        match stmt:
            case PrintStmt():
                self.execute_printstmt(stmt)
            case ExprStmt():
                self.execute_exprstmt(stmt)
            case VarDeclStmt():
                self.execute_vardeclstmt(stmt)
            case BlockStmt():
                self.execute_blockstmt(stmt)
            case IfStmt():
                self.execute_ifstmt(stmt)
            case WhileStmt():
                self.execute_whilestmt(stmt)
            case BreakStmt():
                self.execute_breakstmt(stmt)
            case ContStmt():
                self.execute_contstmt(stmt)
            case FunDeclStmt():
                self.execute_fundeclstmt(stmt)
            case ReturnStmt():
                self.execute_returnstmt(stmt)
            case _:
                self.error(stmt, "Invalid statement")
            
    def execute_fundeclstmt(self, stmt:FunDeclStmt):
        function = FCFunction(stmt, self.environment)
        self.environment.define(stmt.name.value, function)
        return None
    
    def execute_returnstmt(self, stmt:ReturnStmt):
        value = None
        if stmt.value:
            value = self.evaluate(stmt.value)
        raise returnException(value)
    
    def execute_printstmt(self, stmt:PrintStmt):
        value = self.evaluate(stmt.expr)
        print(str(value))
        return None
    
    def execute_exprstmt(self, stmt:ExprStmt):
        value = self.evaluate(stmt.expr)
        return None
    
    def execute_blockstmt(self, stmt:BlockStmt, envr:Environment=None):
        previous_env = self.environment

        if envr is not None:
            # when you pass environment that would the parent env but
            # after execution what would be the env ?
            # it should be self.environment not envr
            parent_env = envr
        else:
            parent_env = self.environment

        child_env = Environment(parent = parent_env)
        
        self.environment = child_env
        try:
            for statement in stmt.statments:
                self.execute(statement)
        finally:
            self.environment = previous_env

        return None

    def execute_vardeclstmt(self, var:VarDeclStmt):
        value = None
        if var.initializer is not None:
            value = self.evaluate(var.initializer)
        self.environment.define(var.name, value)


    def execute_ifstmt(self, stmt:IfStmt):
        if self.evaluate(stmt.condition):
            self.execute(stmt.thenBranch)
        elif stmt.elseBranch is not None:
            self.execute(stmt.elseBranch)

    def execute_whilestmt(self, stmt:WhileStmt):
        if self.int_args(self.evaluate(stmt.condition), 0):
            while self.evaluate(stmt.condition):
                try:
                    self.execute(stmt.thenBranch)
                except breakException as e:
                    break
                except contException as e:
                    if stmt.increment:
                        self.evaluate(stmt.increment)
                    continue

    def execute_breakstmt(self, stmt:BreakStmt):
        raise breakException("break")
    
    def execute_contstmt(self, stmt:BreakStmt):
        raise contException("continue")

    def evaluate(self, expr:Binary | Unary | Literal | Grouping | Identifier | Assignment | Call):
        match expr:
            case Binary():
                return self.evaluate_binary(expr)
            case Unary():
                return self.evaluate_unary(expr)
            case Grouping():
                return self.evaluate_grouping(expr)  
            case Literal():
                return self.evaluate_literal(expr) 
            case Identifier():
                return self.evaluate_identifier(expr) 
            case Assignment():
                return self.evaluate_assign(expr)
            case Logical():
                return self.evaluate_logical(expr)
            case Call():
                return self.evaluate_call(expr)
            case _:
                return self.error(expr, "Unknown Type")
    
    def evaluate_call(self, expr:Call):
        callee = self.evaluate(expr.callee)

        arguments = []
        for arg in expr.args:
            arguments.append(self.evaluate(arg))

        if not isinstance(callee, (FCCallable, FCFunction)):
            self.error(expr, "can only call function and classes")

        if (len(arguments) != callee.arity()):
            self.error(expr, f"expected {callee.arity()} args but got {len(arguments())}")
        return callee.call(self, arguments)
    
    def evaluate_logical(self, expr:Logical):
        left = self.evaluate(expr.left)

        match expr.operator.type:
            case TokenType.OR:
                if self.int_args(left, 0):
                    return left
            case TokenType.AND:
                if self.int_args(left, 0):
                    return left
        
        return self.evaluate(expr.right)
    
    def evaluate_assign(self, expr:Assignment):
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value
    
    def evaluate_binary(self, expr:Binary):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case TokenType.MINUS:
                if self.int_args(left, right):
                    return left - right
                self.error(expr, "Can not minus type other NUMERIC")
            
            case TokenType.PLUS:
                if self.int_args(left, right):
                    return left + right
                if self.str_args(left, right):
                    return str(left + right)
                self.error(expr, f"Can not add not int {left} + {right}")
            case TokenType.STAR:
                if self.int_args(left, right):
                    return left * right
                self.error(expr, "Can not multiply type other NUMERIC")
            case TokenType.SLASH:
                if self.int_args(left, right):
                    return left / right
                self.error(expr, "Can not divide type other NUMERIC")
            
            case TokenType.EQUAL_EQUAL:
                if self.int_args(left, right):
                    return int(left) == int(right)
                self.error(expr, "Can not compare (==) type other NUMERIC")
            case TokenType.BANG_EQUAL:
                if self.int_args(left, right):
                    return int(left) != int(right)
                self.error(expr, "Can not compare (!=) type other NUMERIC")

            case TokenType.LESS:
                if self.int_args(left, right):
                    return int(left) < int(right)
                self.error(expr, "Can not compare (<) type other NUMERIC")
            case TokenType.LESS_EQUAL:
                if self.int_args(left, right):
                    return int(left) <= int(right)
                self.error(expr, "Can not compare (<=) type other NUMERIC")
            case TokenType.GREATER:
                if self.int_args(left, right):
                    return int(left) > int(right)
                self.error(expr, "Can not compare (>) type other NUMERIC")
            case TokenType.GREATER_EQUAL:
                if self.int_args(left, right):
                    return int(left) >= int(right)
                self.error(expr, "Can not compare (>=) type other NUMERIC")
            case _:
                self.error(expr, "Wrong identifier")

    def evaluate_unary(self, expr:Unary):
        right = self.evaluate(expr.right)
        if not self.int_args(1, right):
            self.error(expr, "Non Numeric unary operation not permitted")

        match expr.operator.type:
            case TokenType.MINUS:
                return -right
            case TokenType.BANG:
                return self.invert(right)
        
    def evaluate_literal(self, expr:Literal):
        if isinstance(expr.value, str):
            return expr.value
        if expr.value == None:
            return None
        return int(expr.value)
        
    def evaluate_grouping(self, expr:Grouping):
        return self.evaluate(expr.expr)
    
    def evaluate_identifier(self, expr:Identifier):
        return self.environment.get(expr.token.value)
    
    def int_args(self, left, right):
        if left == None or right == None:
            return False
        
        if isinstance(left, (int, float, bool)) and isinstance(right, (int, float, bool)):
            return True 
        
        return False
        
    def str_args(self, left, right):
        if isinstance(left, str) and isinstance(right, str):
            return True
        return False
        
    def invert(self ,right):
        if isinstance(right, int) or isinstance(right, float):
            if float(right) == 0.0:
                return True;
            else:
                return False;

    def error(self, expr:Expr | Stmt, message:str):
        token = None
        match expr:
            case Expr():
                token = self.token_from_expr(expr)
            case Stmt():
                token = self.token_from_stmt(expr)

        self.has_error = True

        if token and self.source:
            print(f"\n! Runtime Error:")
            print(f"  {self.filepath}:{token.line+1}:{token.column}")

            lines = self.source.split('\n')
            line = lines[token.line] if token.line < len(lines) else ""
            column = token.column - len(token.value)

            prefix = f"  {token.line+1} | "
            print(f"{prefix}{line}")
            print(f"{' ' * len(prefix)}{' ' * column}^")
            print(f"  {message}\n")
        else:
            print(f"\n! Runtime Error:")
            print(f"  {message}\n")

        raise Exception(message)

    def token_from_expr(self, expr) -> Token | None:
        match expr:
            case Binary():
                return expr.operator
            case Unary():
                return expr.operator
            case Logical():
                return expr.operator
            case Identifier():
                return expr.token
            case Assignment():
                return self.token_from_expr(expr.value)
            case Grouping():
                return self.token_from_expr(expr.expr)
            case Literal():
                return None
        return None

    def token_from_stmt(self, stmt) -> Token | None:
        match stmt:
            case PrintStmt():
                return self.token_from_expr(stmt.expr)
            case ExprStmt():
                return self.token_from_expr(stmt.expr)
            case VarDeclStmt():
                return self.token_from_expr(stmt.initializer) if stmt.initializer else None
            case IfStmt():
                return self.token_from_expr(stmt.condition)
            case WhileStmt():
                return self.token_from_expr(stmt.condition)
            case BlockStmt():
                return None
        return None