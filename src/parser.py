from .helper import Token, TokenType
from .expressions import (
    Binary, 
    Unary, 
    Grouping,
    Literal,
    Identifier, 
    Assignment,
    Logical
)
from .statements import (
    PrintStmt, 
    ExprStmt, 
    VarDeclStmt,
    BlockStmt,
    IfStmt,
    WhileStmt,
    BreakStmt,
    ContStmt
)


class Paser:
    def __init__(self, tokens:list[Token], source:str, filepath:str):
        self.tokens = tokens
        self.current_token_index = 0
        self.source = source
        self.filename = filepath
        self.has_error = False

    def parse(self):
        self.statements = []
        try:
            while not self.isAtEnd():
                stmt = self.statement()
                if stmt is not None:
                    self.statements.append(stmt)

                if self.has_error:
                    return self.statements
        except Exception as e:
            self.has_error = True

        return self.statements
        
    
    def statement(self):
        if self.match([TokenType.IF]):
            return self.ifStmt()
        if self.match([TokenType.WHILE]):
            return self.whileStmt()
        if self.match([TokenType.FOR]):
            return self.forStmt()
        if self.match([TokenType.VAR]):
            return self.varDeclStatement()
        if self.match([TokenType.PRINT]):
            return self.printStatement()
        if self.match([TokenType.OPEN_BRACE]):
            return self.blockStatement()
        if self.match([TokenType.BREAK]):
            return self.breakStatement()
        if self.match([TokenType.CONTINUE]):
            return self.contStatement()
        if self.match([TokenType.COMMENT]):
            return None
        if self.match([TokenType.MULTILINE_COMMENT]):
            return None
        return self.expressionStatement()
    
    def ifStmt(self):
        self.consume(TokenType.OPEN_PAR, "Expected ( after if")
        condition = self.expression()
        self.consume(TokenType.CLOSE_PAR, "Expected ) after condition")
        
        thenBranch = self.statement()
        elseBranch = None

        if (self.match([TokenType.ELSE])):
            elseBranch = self.statement()

        return IfStmt(condition, thenBranch, elseBranch)
    
    def whileStmt(self):
        self.consume(TokenType.OPEN_PAR, "Expected ( after while")
        condition = self.expression()
        self.consume(TokenType.CLOSE_PAR, "Expected ) after condition")
        
        thenBranch = self.statement()

        return WhileStmt(condition, thenBranch)
    
    def forStmt(self):
        self.consume(TokenType.OPEN_PAR, "Expected ( after for")
        
        initializer = None
        if self.match([TokenType.SEMICOLON]):
            initializer = None
        elif self.match([TokenType.VAR]):
            initializer = self.varDeclStatement()
        else:
            initializer = self.expressionStatement()

        condition = None
        if not self.check(TokenType.SEMICOLON):
            condition = self.expression()
        self.consume(TokenType.SEMICOLON, "expected ; after for condition")
        

        increment = None
        if not self.check(TokenType.CLOSE_PAR):
            increment = self.expression()
        self.consume(TokenType.CLOSE_PAR, "expected ) after for clauses")

        thenBranch = self.statement()

        if increment is not None:
            thenBranch.statments.append(ExprStmt(increment))

        if condition is None:
            condition = Literal(1)

        while_stmt = WhileStmt(condition, thenBranch, increment)

        if initializer is not None:
            block_list = [initializer, while_stmt]
            while_stmt = BlockStmt(block_list)

        return while_stmt

    def varDeclStatement(self):
        name_token = self.consume(TokenType.IDENTIFIER, "Expect variable name").value
        initializer = None
        if self.match([TokenType.EQUAL]):
            initializer = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ; after expression")
        return VarDeclStmt(name_token, initializer)
    
    def printStatement(self):
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expected ; after value")
        return PrintStmt(value)
    
    def expressionStatement(self):
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expected ; after expression")
        return ExprStmt(value)
    
    def blockStatement(self):
        statements = []
        while not self.check(TokenType.CLOSE_BRACE):
            statements.append(self.statement())
        self.consume(TokenType.CLOSE_BRACE, "Expect } after block")
        return BlockStmt(statements)
    
    def breakStatement(self):
        self.consume(TokenType.SEMICOLON, "Expected Semicolon after break");
        return BreakStmt()
    
    def contStatement(self):
        self.consume(TokenType.SEMICOLON, "Expected Semicolon after continue");
        return ContStmt()
    
    def validate(self):
        if not self.isAtEnd():
            self.error(self.peek(), "Unexpected Token")
            return False
        return True
        
    def expression(self):
        return self.assignment()
    
    def assignment(self):
        expr = self.logical_or();

        if self.match([TokenType.EQUAL]):
            equals = self.previous()
            # calling assignment cause we want to support
            # a = b = c = 4 like this
            value = self.assignment()
            if isinstance(expr, Identifier):
                return Assignment(expr.token.value, value)
            
            self.error(self.peek(), "Invalid assignment target.")

        return expr
    
    def logical_or(self):
        expr = self.logical_and()

        while self.match([TokenType.OR]):
            operetor = self.previous()
            right = self.logical_and()
            expr = Logical(expr, operetor, right)

        return expr
    
    def logical_and(self):
        expr = self.equality()

        while self.match([TokenType.AND]):
            operetor = self.previous()
            right = self.equality()
            expr = Logical(expr, operetor, right)

        return expr
    
    def equality(self):
        # print("equality called now calling comparison")
        expr = self.comparison()
        # print("comparison call finish from equality")

        while self.match([TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL]):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)

        return expr

    def comparison(self):
        # print("comparison called now calling term")
        expr = self.term()
        # print("term call finish from comparison")

        while self.match([TokenType.GREATER, TokenType.LESS, TokenType.GREATER_EQUAL, TokenType.LESS_EQUAL]):
            operator = self.previous();
            right = self.term();
            expr = Binary(expr, operator, right)

        return expr

    def term(self):
        # print("term called now calling factor")
        expr  = self.factor()
        # print("factor call finish from term")

        while self.match([TokenType.PLUS, TokenType.MINUS]):
            operator = self.previous();
            right = self.factor();
            expr = Binary(expr, operator, right)

        return expr

    def factor(self):
        # print("factor called now calling unary")
        expr = self.unary()
        # print("unary call finish from factor")

        while self.match([TokenType.SLASH, TokenType.STAR]):
            operator = self.previous();
            right = self.unary();
            expr = Binary(expr, operator, right)

        return expr

    def unary(self):
        if self.match([TokenType.MINUS, TokenType.BANG]):
            operator = self.previous();
            right = self.unary();
            expr = Unary(operator, right)
            return expr
        return self.primary()

    def primary(self):
        if self.match([TokenType.TRUE]):
            return Literal(int(1))
        if self.match([TokenType.FALSE]):
            return Literal(int(0))
        if self.match([TokenType.NIL]):
            return Literal(None)

        if self.match([TokenType.CONSTANT, TokenType.STRING]):
            return Literal(self.previous().value)
        
        if self.match([TokenType.IDENTIFIER]):
            return Identifier(self.previous())
        
        if self.match([TokenType.OPEN_PAR]):
            expr = self.expression()
            self.consume(TokenType.CLOSE_PAR, "No closing ) found !")
            return Grouping(expr)    
        
        self.error(self.peek(), "Expected Expression !")

    def synchronize(self):
        self.advance()

        while not self.isAtEnd():
            if self.previous().type == TokenType.SEMICOLON:
                return
        
            match self.peek().type:
                case TokenType.CLASS:
                    return
                case TokenType.FUN:
                    return
                case TokenType.VAR:
                    return
                case TokenType.FOR:
                    return
                case TokenType.IF:
                    return
                case TokenType.WHILE:
                    return
                case TokenType.FOR:
                    return
                case TokenType.PRINT:
                    return
                case TokenType.RETURN:
                    return
            
            self.advance()
        

    def previous(self):
        if self.current_token_index > 0:
            return self.tokens[self.current_token_index - 1]
        return None
    
    def match(self, tokentypes:list):
        if self.isAtEnd():
            return False
        
        if self.tokens[self.current_token_index].type in tokentypes:
            self.advance()
            return True
        return False

    def advance(self):   
        current_value = self.tokens[self.current_token_index]     
        self.current_token_index += 1

        if self.isAtEnd():
            return None
        
        return current_value
    
    def isAtEnd(self):
        if self.current_token_index >= len(self.tokens):
            return True
        if self.tokens[self.current_token_index].type == TokenType.EOF:
            return True
        return False
    
    def consume(self, type:TokenType, message:str):
        if self.check(type):
            return self.advance()
        self.error(self.peek(), message)
        
    def check(self, type):
        if self.isAtEnd():
            return False
        
        if self.tokens[self.current_token_index].type == type:
            return True
        return False

    def peek(self, step:int=0):
        if self.isAtEnd():
            return None
        index = step + self.current_token_index
        return self.tokens[index]

    def error(self, token:Token, message:str):
        if token is None:
            print(f"\n! Parse Error:")
            print(f"{self.filename}:eof")
            print(f"  {message}\n")
        else:
            print(f"\n! Parse Error:")
            print(f"{self.filename}:{token.line+1}:{token.column}")

            lines = self.source.split('\n')
            line = lines[token.line] if token.line < len(lines) else ""
            column = token.column - len(token.value)

            prefix = f"{token.line+1} | "
            print(f"{prefix}{line}")
            print(f"{' ' * len(prefix)}{' ' * column}^")
            print(f"  {message}\n")

        self.has_error = True

        raise Exception(message)