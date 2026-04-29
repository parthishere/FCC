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
    
    def get(self, name):
        if name in self.values:
            return self.values.get(name)
        
        if self.parent != None:
            return self.parent.get(name)

        return None