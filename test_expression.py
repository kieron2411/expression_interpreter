import unittest
from expression import Constant, Variable, Add

class TestExpression(unittest.TestCase):
    #test Constant
    def test_constant_eval(self):
        const = Constant(5)
        self.assertEqual(const.eval({"x": 3}), 5)
    def test_constant_diff(self):
        const = Constant(5)
        self.assertEqual(const.diff("x"), Constant(0))
    def test_constant_repr(self):
        const = Constant(5)
        self.assertEqual(const.__repr__(), "Constant(5)")
    def test_constant_str(self):
        const = Constant(5)
        self.assertEqual(const.__str__(), "5")
    def test_constant_neq(self):
        const1 = Constant(5)
        const2 = Constant(6)
        self.assertNotEqual(const1, const2)

    #test Variable
    def test_variable_eval(self):
        var = Variable("x")
        self.assertEqual(var.eval({"x": 3}), 3)
    def test_variable_diff_same(self):
        var = Variable("x")
        self.assertEqual(var.diff("x"), Constant(1))
    def test_variable_diff_different(self):
        var = Variable("x")
        self.assertEqual(var.diff("y"), Constant(0))
    def test_variable_repr(self):
        var = Variable("x")
        self.assertEqual(var.__repr__(), 'Variable("x")')
    def test_variable_str(self):
        var = Variable("x")
        self.assertEqual(var.__str__(), "x")
    def test_variable_neq(self):
        var1 = Variable("x")
        var2 = Variable("y")
        self.assertNotEqual(var1, var2)

    #test Add
    def test_add_eval1(self):
        expr = Add(Constant(5), Constant(3))
        self.assertEqual(expr.eval({"x": 3}), 8)
    def test_add_eval2(self):
        expr = Add(Constant(5), Variable("x"))
        self.assertEqual(expr.eval({"x": 3}), 8)
    def test_add_eval3(self):
        expr = Add(Variable("x"), Variable("y"))
        self.assertEqual(expr.eval({"x": 3, "y":4.5}), 7.5)
    def test_add_diff1(self):
        expr = Add(Constant(5), Constant(3))
        self.assertEqual(expr.diff("x"), Add(Constant(0), Constant(0)))
    def test_add_diff2(self):
        expr = Add(Constant(5), Variable("x"))
        self.assertEqual(expr.diff("x"), Add(Constant(0), Constant(1)))
    def test_add_diff3(self):
        expr = Add(Variable("x"), Variable("y"))
        self.assertEqual(expr.diff("x"), Add(Constant(1), Constant(0)))
    def test_add_repr(self):
        expr = Add(Constant(5), Variable("x"))
        self.assertEqual(expr.__repr__(), 'Add(Constant(5), Variable("x"))')
    def test_add_str(self):
        expr = Add(Constant(5), Variable("x"))
        self.assertEqual(expr.__str__(), "5 + x")
    def test_add_neq(self):
        expr1 = Add(Constant(5), Variable("x"))
        expr2 = Add(Constant(5), Variable("y"))
        self.assertNotEqual(expr1, expr2)