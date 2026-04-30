import time 

from .callable import FCCallable


class Clock(FCCallable):
    def __init__(self):
        pass

    def arity(self):
        return 0
    
    def call(self, interpreter, arguments):
        return time.time_ns() // 1_000_000 # time in ms

    def __repr__(self):
        return "<native fn : clock>"