import time 

from .callable import FCCallable


class ClockMS(FCCallable):
    name = "clock_ms"
    def __init__(self):
        pass

    def call(self, interpreter, arguments):
        return time.time_ns() / 1_000_000 # time in ms
    
    def arity(self):
        return 0

    def __repr__(self):
        return "<native fn : clock_ms>"
    
class ClockUS(FCCallable):
    name = "clock_us"
    def __init__(self):
        pass

    def call(self, interpreter, arguments):
        return time.time_ns() / 1_000 # time in us
    
    def arity(self):
        return 0

    def __repr__(self):
        return "<native fn : clock_us>"
    
class ClockNS(FCCallable):
    name = "clock_ns"
    def __init__(self):
        pass

    def call(self, interpreter, arguments):
        return time.time_ns()
    
    def arity(self):
        return 0

    def __repr__(self):
        return "<native fn : clock_ns>"