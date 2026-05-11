from .environment import Environment

from .statements import FunDeclStmt

class FCCallable:
    def __init__(self):
        pass
    
    def call(self, interpreter, arguments):
        pass
    
    def arity(self):
        return 0

class FCFunction(FCCallable):

    def __init__(self, declaration:FunDeclStmt, closure:Environment):
        self.declaration = declaration
        self.closure = closure

    def call(self, interpreter:Interpret, arguments:list):
        from .interpreter import returnException

        environment = Environment(self.closure) 

        for index, param in enumerate(self.declaration.parameters):
            environment.define(param.value, arguments[index])

        try:
            interpreter.execute_blockstmt(self.declaration.body, environment)
        except returnException as e:
            return e.args[0]

    def arity(self):
        return len(self.declaration.parameters)
    
    def __repr__(self):
        return f"< fn {self.declaration} >"