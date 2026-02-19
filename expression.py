import math

class Expr:
    def eval(self, env):
        raise(NotImplementedError)  
    def diff(self, var):
        raise(NotImplementedError)
    def simplify(self):
        raise(NotImplementedError)
    def __repr__(self):
        raise(NotImplementedError)
    def __str__(self):
        raise(NotImplementedError)
    def __eq__(self):
        raise(NotImplementedError)
    

class Constant(Expr):
    def __init__(self, value):
        self.value = value
    def eval(self, env):
        return self.value
    def diff(self, var):
        return Constant(0)
    def simplify(self):
        return self
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
    def simplify(self):
        return self
    def __repr__(self):
        return f'Variable("{self.name}")'
    def __str__(self):
        return self.name
    def __eq__(self, other):
        return isinstance(other, Variable) and self.name == other.name
    

class Add(Expr):
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2
    def eval(self, env):
        return self.expr1.eval(env) + self.expr2.eval(env) 
    def diff(self, var):
        return Add(self.expr1.diff(var), self.expr2.diff(var))
    def simplify(self):
        expr1 = self.expr1.simplify()
        expr2 = self.expr2.simplify()
        if isinstance(expr1, Constant) and expr1.value == 0:
            return expr2
        if expr2 == Constant(0):
            return expr1
        if isinstance(expr1, Constant) and isinstance(expr2, Constant):
            return Constant(expr1.value + expr2.value)
        return Add(expr1, expr2)
    def __repr__(self):
        return f"Add({self.expr1.__repr__()}, {self.expr2.__repr__()})"    
    def __str__(self):
        return f"({self.expr1.__str__()} + {self.expr2.__str__()})"
    def __eq__(self, other):
        return isinstance(other, Add) and self.expr1 == other.expr1 and self.expr2 == other.expr2
        #commutativity not implemented currently


class Sub(Expr):
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2
    def eval(self, env):
        return self.expr1.eval(env) - self.expr2.eval(env)
    def diff(self, var):
        return Sub(self.expr1.diff(var), self.expr2.diff(var))
    def simplify(self):
        expr1 = self.expr1.simplify()
        expr2 = self.expr2.simplify()
        if isinstance(expr2, Constant) and expr2.value == 0:
            return expr1
        if isinstance(expr1, Constant) and isinstance(expr2, Constant):
            return Constant(expr1.value - expr2.value)
        return Sub(expr1, expr2)
    def __repr__(self):
        return f"Sub({self.expr1.__repr__()}, {self.expr2.__repr__()})"
    def __str__(self):
        return f"({self.expr1.__str__()} - {self.expr2.__str__()})"
    def __eq__(self, other):
        return isinstance(other, Sub) and self.expr1 == other.expr1 and self.expr2 == other.expr2
    

class Mul(Expr):
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2
    def eval(self, env):
        return self.expr1.eval(env) * self.expr2.eval(env)
    def diff(self, var):
        return Add(
            Mul(self.expr1, self.expr2.diff(var)),
            Mul(self.expr1.diff(var), self.expr2)
        )
    def simplify(self):
        expr1 = self.expr1.simplify()
        expr2 = self.expr2.simplify()
        if isinstance(expr1, Constant) and expr1.value == 0:
            return Constant(0)
        if isinstance(expr2, Constant) and expr2.value == 0:
            return Constant(0)
        if isinstance(expr1, Constant) and expr1.value == 1:
            return expr2
        if isinstance(expr2, Constant) and expr2.value == 1:
            return expr1
        if isinstance(expr1, Constant) and isinstance(expr2, Constant):
            return Constant(expr1.value * expr2.value)
        return Mul(expr1, expr2)
    def __repr__(self):
        return f"Mul({self.expr1.__repr__()}, {self.expr2.__repr__()})"
    def __str__(self):
        return f"({self.expr1.__str__()} * {self.expr2.__str__()})"
    def __eq__(self, other):
        return isinstance(other, Mul) and self.expr1 == other.expr1 and self.expr2 == other.expr2
    

class Div(Expr):
    def __init__(self, expr1, expr2):
        if isinstance(expr2, Constant) and expr2.value == 0:
            raise ZeroDivisionError("Division by 0 is not valid")
        self.expr1 = expr1
        self.expr2 = expr2
    def eval(self, env):
        return self.expr1.eval(env) / self.expr2.eval(env)
    def diff(self, var):
        return Div(
            Sub(
                Mul(self.expr1.diff(var), self.expr2),
                Mul(self.expr1, self.expr2.diff(var))
            ),
            Mul(self.expr2, self.expr2)
        )
    def simplify(self):
        expr1 = self.expr1.simplify()
        expr2 = self.expr2.simplify()
        if isinstance(expr2, Constant) and expr2.value == 0:
            raise ZeroDivisionError("Division by 0 is not valid")
        if isinstance(expr1, Constant) and expr1.value == 0:
            return Constant(0)
        if isinstance(expr2, Constant) and expr2.value == 1:
            return expr1
        if isinstance(expr1, Constant) and isinstance(expr2, Constant):
            return Constant(expr1.value / expr2.value)
        return Div(expr1, expr2)
    def __repr__(self):
        return f"Div({self.expr1.__repr__()}, {self.expr2.__repr__()})"
    def __str__(self):
        return f"({self.expr1.__str__()} / {self.expr2.__str__()})"
    def __eq__(self, other):
        return isinstance(other, Div) and self.expr1 == other.expr1 and self.expr2 == other.expr2
    

class Log(Expr):
    def __init__(self, expr):
        self.expr = expr
    def eval(self, env):
        return math.log(self.expr.eval(env))
    def diff(self, var):
        return Div(self.expr.diff(var), self.expr)
    def simplify(self):
        expr = self.expr.simplify()
        if isinstance(expr, Constant):
            return Constant(math.log(expr.value))
        return Log(expr)
    def __repr__(self):
        return f"Log({self.expr.__repr__()})"
    def __str__(self):
        return f"log({self.expr.__str__()})"
    def __eq__(self, other):
        return isinstance(other, Log) and self.expr == other.expr
    

class Pow(Expr):
    def __init__(self, base, exp):
        self.base = base
        self.exp = exp
    def eval(self, env):
        return self.base.eval(env) ** self.exp.eval(env)
    def diff(self, var):
        return Mul(
            Pow(self.base, self.exp),
            Add(
                Div(
                    Mul(self.exp, self.base.diff(var)),
                    self.base
                ),
                Mul(
                    self.exp.diff(var),
                    Log(self.base)
                )
            )
        )
    def simplify(self):
        base = self.base.simplify()
        exp = self.exp.simplify()
        if isinstance(exp, Constant) and exp.value == 1:
            return base
        if isinstance(exp, Constant) and exp.value == 0:
            return Constant(1)
        if isinstance(base, Constant) and isinstance(exp, Constant):
            return Constant(base.value ** exp.value)
        return Pow(base, exp)
    def __repr__(self):
        return f"Pow({self.base.__repr__()}, {self.exp.__repr__()})"
    def __str__(self):
        return f"({self.base.__str__()} ^ {self.exp.__str__()})"
    def __eq__(self, other):
        return isinstance(other, Pow) and self.base == other.base and self.exp == other.exp
    

class Sin(Expr):
    def __init__(self, expr):
        self.expr = expr
    def eval(self, env):
        return math.sin(self.expr.eval(env))
    def diff(self, var):
        return Mul(self.expr.diff(var), Cos(self.expr))
    def simplify(self):
        expr = self.expr.simplify()
        if isinstance(expr, Constant):
            return Constant(math.sin(expr.value))
        return Sin(expr)
    def __repr__(self):
        return f"Sin({self.expr.__repr__()})"
    def __str__(self):
        return f"sin({self.expr.__str__()})"
    def __eq__(self, other):
        return isinstance(other, Sin) and self.expr == other.expr


class Cos(Expr):
    def __init__(self, expr):
        self.expr = expr
    def eval(self, env):
        return math.cos(self.expr.eval(env))
    def diff(self, var):
        return Mul(
            Constant(-1),
            Mul(self.expr.diff(var), Sin(self.expr))
        )
    def simplify(self):
        expr = self.expr.simplify()
        if isinstance(expr, Constant):
            return Constant(math.cos(expr.value))
        return Cos(expr)
    def __repr__(self):
        return f"Cos({self.expr.__repr__()})"
    def __str__(self):
        return f"cos({self.expr.__str__()})"
    def __eq__(self, other):
        return isinstance(other, Cos) and self.expr == other.expr