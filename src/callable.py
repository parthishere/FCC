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
    def __init__(self, declaration:FunDeclStmt):
        self.declaration = declaration

    def call(self, interpreter, arguments:list):
        environment = Environment(interpreter.global_env)   

        for index, param in enumerate(self.declaration.parameters):
            environment.define(param.value, arguments[index])

        interpreter.execute_blockstmt(self.declaration.body, environment)

    def arity(self):
        return len(self.declaration.parameters)
    
    def __repr__(self):
        return f"< fn {self.declaration} >"