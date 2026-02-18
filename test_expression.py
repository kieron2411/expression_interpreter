import unittest
from expression import (
    Constant, Variable, 
    Add, Sub, Mul, Div
    )

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
    def test_constant_eq(self):
        const1 = Constant(5)
        const2 = Constant(5)
        self.assertEqual(const1, const2)
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
    def test_variable_eq(self):
        var1 = Variable("x")
        var2 = Variable("x")
        self.assertEqual(var1, var2)
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
        self.assertEqual(expr.__str__(), "(5 + x)")
    def test_add_eq(self):
        expr1 = Add(Constant(5), Variable("x"))
        expr2 = Add(Constant(5), Variable("x"))
        self.assertEqual(expr1, expr2)
    def test_add_neq(self):
        expr1 = Add(Constant(5), Variable("x"))
        expr2 = Add(Constant(5), Variable("y"))
        self.assertNotEqual(expr1, expr2)

    #test Sub
    def test_sub_eval1(self):
        expr = Sub(Constant(5), Constant(3))
        self.assertEqual(expr.eval({"x": 3}), 2)
    def test_sub_eval2(self):
        expr = Sub(Constant(5), Variable("x"))
        self.assertEqual(expr.eval({"x": 3}), 2)
    def test_sub_eval3(self):
        expr = Sub(Variable("x"), Variable("y"))
        self.assertEqual(expr.eval({"x": 3, "y": 4.5}), -1.5)
    def test_sub_diff1(self):
        expr = Sub(Constant(5), Constant(3))
        self.assertEqual(expr.diff("x"), Sub(Constant(0), Constant(0)))
    def test_sub_diff2(self):
        expr = Sub(Constant(5), Variable("x"))
        self.assertEqual(expr.diff("x"), Sub(Constant(0), Constant(1)))
    def test_sub_diff3(self):
        expr = Sub(Variable("x"), Variable("y"))
        self.assertEqual(expr.diff("x"), Sub(Constant(1), Constant(0)))
    def test_sub_repr(self):
        expr = Sub(Constant(5), Variable("x"))
        self.assertEqual(expr.__repr__(), 'Sub(Constant(5), Variable("x"))')
    def test_sub_str(self):
        expr = Sub(Constant(5), Variable("x"))
        self.assertEqual(expr.__str__(), "(5 - x)")
    def test_sub_eq(self):
        expr1 = Sub(Constant(5), Variable("x"))
        expr2 = Sub(Constant(5), Variable("x"))
        self.assertEqual(expr1, expr2)
    def test_sub_neq(self):
        expr1 = Sub(Constant(5), Variable("x"))
        expr2 = Sub(Constant(5), Variable("y"))
        self.assertNotEqual(expr1, expr2)

    #test Mul
    def test_mul_eval1(self):
        expr = Mul(Constant(5), Constant(3))
        self.assertEqual(expr.eval({"x": 3}), 15)
    def test_mul_eval2(self):
        expr = Mul(Constant(5), Variable("x"))
        self.assertEqual(expr.eval({"x": 3}), 15)
    def test_mul_eval3(self):
        expr = Mul(Variable("x"), Variable("y"))
        self.assertEqual(expr.eval({"x": 3, "y": 4.5}), 13.5)
    def test_mul_diff1(self):
        expr = Mul(Constant(5), Constant(3))
        expected = Add(
            Mul(Constant(5), Constant(0)),
            Mul(Constant(0), Constant(3))
        )
        self.assertEqual(expr.diff("x"), expected)
    def test_mul_diff2(self):
        expr = Mul(Constant(5), Variable("x"))
        expected = Add(
            Mul(Constant(5), Constant(1)),
            Mul(Constant(0), Variable("x"))
        )
        self.assertEqual(expr.diff("x"), expected)
    def test_mul_diff3(self):
        expr = Mul(Variable("x"), Variable("y"))
        expected = Add(
            Mul(Variable("x"), Constant(0)),
            Mul(Constant(1), Variable("y"))
        )
        self.assertEqual(expr.diff("x"), expected)
    def test_mul_repr(self):
        expr = Mul(Constant(5), Variable("x"))
        self.assertEqual(expr.__repr__(), 'Mul(Constant(5), Variable("x"))')
    def test_mul_str(self):
        expr = Mul(Constant(5), Variable("x"))
        self.assertEqual(expr.__str__(), "(5 * x)")
    def test_mul_eq(self):
        expr1 = Mul(Constant(5), Variable("x"))
        expr2 = Mul(Constant(5), Variable("x"))
        self.assertEqual(expr1, expr2)
    def test_mul_neq(self):
        expr1 = Mul(Constant(5), Variable("x"))
        expr2 = Mul(Constant(5), Variable("y"))
        self.assertNotEqual(expr1, expr2)

    #test Div
    def test_div_eval1(self):
        expr = Div(Constant(5), Constant(4))
        self.assertEqual(expr.eval({"x": 3}), 1.25)
    def test_div_eval2(self):
        expr = Div(Constant(5), Variable("x"))
        self.assertAlmostEqual(expr.eval({"x": 3}), 5 / 3)
    def test_div_eval3(self):
        expr = Div(Variable("x"), Variable("y"))
        self.assertEqual(expr.eval({"x": 4, "y": 5}), 0.8)
    def test_div_diff1(self):
        expr = Div(Constant(5), Constant(3))
        expected = Div(
            Sub(
                Mul(Constant(0), Constant(3)),
                Mul(Constant(5), Constant(0))
            ),
            Mul(Constant(3), Constant(3))
        )
        self.assertEqual(expr.diff("x"), expected)
    def test_div_diff2(self):
        expr = Div(Constant(5), Variable("x"))
        expected = Div(
            Sub(
                Mul(Constant(0), Variable("x")),
                Mul(Constant(5), Constant(1))
            ),
            Mul(Variable("x"), Variable("x"))
        )
        self.assertEqual(expr.diff("x"), expected)
    def test_div_diff3(self):
        expr = Div(Variable("x"), Variable("y"))
        expected = Div(
            Sub(
                Mul(Constant(1), Variable("y")),
                Mul(Variable("x"), Constant(0))
            ),
            Mul(Variable("y"), Variable("y"))
        )
        self.assertEqual(expr.diff("x"), expected)
    def test_div_repr(self):
        expr = Div(Constant(5), Variable("x"))
        self.assertEqual(expr.__repr__(), 'Div(Constant(5), Variable("x"))')
    def test_div_str(self):
        expr = Div(Constant(5), Variable("x"))
        self.assertEqual(expr.__str__(), "(5 / x)")
    def test_div_eq(self):
        expr1 = Div(Constant(5), Variable("x"))
        expr2 = Div(Constant(5), Variable("x"))
        self.assertEqual(expr1, expr2)
    def test_div_neq(self):
        expr1 = Div(Constant(5), Variable("x"))
        expr2 = Div(Constant(5), Variable("y"))
        self.assertNotEqual(expr1, expr2)

    #test nested expressions
    def test_add_in_add_eval(self):
        expr = Add(
            Add(Constant(5), Variable("x")),
            Add(Constant(3), Variable("y"))
        )
        self.assertEqual(expr.eval({"x": 4, "y": -2}), 10)
    def test_add_in_add_diff(self):
        expr = Add(
            Add(Constant(5), Variable("x")),
            Add(Constant(3), Variable("y"))
        )
        expected = Add(
            Add(Constant(0), Constant(1)),
            Add(Constant(0), Constant(0))
        )
        self.assertEqual(expr.diff("x"), expected)
    def test_add_in_mul_eval(self):
        expr = Mul(
            Add(Constant(3), Variable("x")),
            Add(Constant(2), Variable("x"))
        )
        self.assertEqual(expr.eval({"x": 4}), 42)
    def test_add_in_mul_diff(self):
        expr = Mul(
            Add(Constant(3), Variable("x")),
            Add(Constant(2), Variable("x"))
        )
        expected = Add(
            Mul(
                Add(Constant(3), Variable("x")),
                Add(Constant(0), Constant(1))
            ),
            Mul(
                Add(Constant(0), Constant(1)),
                Add(Constant(2), Variable("x"))
            )
        )
        self.assertEqual(expr.diff("x"), expected)
    def test_sub_in_add_eval(self):
        expr = Add(
            Sub(Constant(7), Variable("x")),
            Sub(Constant(5), Variable("y"))
        )
        self.assertEqual(expr.eval({"x": 2, "y": -3}), 13)
    def test_sub_in_add_diff(self):
        expr = Add(
            Sub(Constant(7), Variable("x")),
            Sub(Constant(5), Variable("y"))
        )
        expected = Add(
            Sub(Constant(0), Constant(1)),
            Sub(Constant(0), Constant(0))
        )
        self.assertEqual(expr.diff("x"), expected)
    def test_mixed_nest_eval(self):
        expr = Div(
            Mul(
                Sub(Variable("x"), Constant(3)),
                Add(Variable("x"), Constant(2))
            ),
            Add(Constant(1), Variable("x"))
        )
        self.assertEqual(expr.eval({"x": 4}), 1.2)
    def test_mixed_nest_diff(self):
        expr = Div(
            Mul(
                Sub(Variable("x"), Constant(3)),
                Add(Variable("x"), Constant(2))
            ),
            Add(Constant(1), Variable("x"))
        )
        expected = Div(
            Sub(
                Mul(
                    Add(
                        Mul(
                            Sub(Variable("x"), Constant(3)),
                            Add(Constant(1), Constant(0))
                        ),
                        Mul(
                            Sub(Constant(1), Constant(0)),
                            Add(Variable("x"), Constant(2))
                        )
                    ),
                    Add(Constant(1), Variable("x"))
                ),
                Mul(
                    Mul(
                        Sub(Variable("x"), Constant(3)),
                        Add(Variable("x"), Constant(2))
                    ),
                    Add(Constant(0), Constant(1))
                )
            ),
            Mul(
                Add(Constant(1), Variable("x")),
                Add(Constant(1), Variable("x"))
            )
        )
        self.assertEqual(expr.diff("x"), expected)

    def test_div_in_div_eval(self):
        expr = Div(
            Constant(1),
            Add(
                Constant(2), 
                Div(Constant(1), Variable("x"))
            )
        )
        self.assertEqual(expr.eval({"x": 2}), 0.4)

    def test_div_in_div_diff(self):
        expr = Div(
            Constant(1),
            Add(
                Constant(2),
                Div(Constant(1), Variable("x"))
            )
        )
        expected = Div(
            Sub(
                Mul(
                    Constant(0),
                    Add(
                        Constant(2),
                        Div(Constant(1), Variable("x"))
                    )
                ),
                Mul(
                    Constant(1),
                    Add(
                        Constant(0),
                        Div(
                            Sub(
                                Mul(Constant(0), Variable("x")),
                                Mul(Constant(1), Constant(1))
                            ),
                            Mul(Variable("x"), Variable("x"))
                        )
                    )
                )
            ),
            Mul(
                Add(
                    Constant(2),
                    Div(Constant(1), Variable("x"))
                ),
                Add(
                    Constant(2),
                    Div(Constant(1), Variable("x"))
                )
            )
        )
        self.assertEqual(expr.diff("x"), expected)