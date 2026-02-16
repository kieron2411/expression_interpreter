class Expr:
    def eval(self, env):
        raise(NotImplementedError)  
    def diff(self, var):
        raise(NotImplementedError)
    def __repr__(self):
        raise(NotImplementedError)
    def __str__(self):
        raise(NotImplementedError)
    

class Constant(Expr):
    def __init__(self, value):
        self.value = value
    def eval(self, env):
        return self.value
    def diff(self, var):
        return Constant(0)
    def __repr__(self):
        return f"Constant({self.value})"
    def __str__(self):
        return str(self.value)
    def __eq__(self, other):
        return isinstance(other, Constant) and self.value == other.value
    

class Variable(Expr):
    def __init__(self, name):
        self.name = name
    def eval(self, env):
        if self.name in env:
            return env[self.name]
        else:
            raise ValueError(f'Variable "{self.name}" not found in environment')
    def diff(self, var):
        if var == self.name:
            return Constant(1)
        else:
            return Constant(0)
    def __repr__(self):
        return f'Variable("{self.name}")'
    def __str__(self):
        return self.name
    def __eq__(self, other):
        return isinstance(other, Constant) and self.name == other.name
    

class Add(Expr):
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2
    def eval(self, env):
        return self.expr1.eval(env) + self.expr2.eval(env) 
    def diff(self, var):
        return Add(self.expr1.diff(var), self.expr2.diff(var))
    def __repr__(self):
        return f"Add({self.expr1.__repr__()}, {self.expr2.__repr__()})"    
    def __str__(self):
        return f"{self.expr1.__str__()} + {self.expr2.__str__()}"
    def __eq__(self, other):
        return isinstance(other, Add) and self.expr1 == other.expr1 and self.expr2 == other.expr2
        #commutativity not implemented currently