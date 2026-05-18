from .helper import Token, TokenType

class Environment:
    def __init__(self, parent:Environment=None):
        self.values = {}
        self.has_error = False
        self.parent = parent

    def define(self, name, value):
        if name in self.values:
            raise Exception("Redefined Variable")
        self.values.update({name: value})

    def assign(self, name, value):
        if name in self.values:
            self.values.update({name: value})
            return
        
        if self.parent != None:
            self.parent.assign(name, value)
            return

        raise Exception("Undefined Variable")
    
    def assign_at(self, distance:int, name:str, value):
        self.ancestor(distance).values[name] = value
    
    def get(self, name):
        if name in self.values:
            return self.values.get(name)
        
        if self.parent != None:
            return self.parent.get(name)

        return None
    
    def get_at(self, name:str, distance:int):
        return self.ancestor(distance).values[name]
    
    def ancestor(self, distance:int):
        environment = self

        for _ in range(distance):
            environment = environment.parent

        return environment