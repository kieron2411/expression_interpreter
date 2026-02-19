import unittest
import math
from expression import (
    Constant, Variable, 
    Add, Sub, Mul, Div,
    Log, Pow,
    Sin, Cos
    )

class TestExpression(unittest.TestCase):
    #test Constant
    def test_constant_eval(self):
        const = Constant(5)
        self.assertEqual(const.eval({}), 5)
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
        self.assertEqual(expr.eval({}), 8)
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
        self.assertEqual(expr.eval({}), 2)
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
        self.assertEqual(expr.eval({}), 15)
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
        self.assertEqual(expr.eval({}), 1.25)
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

    #test Log
    def test_log_eval1(self):
        expr = Log(Constant(math.e))
        self.assertEqual(expr.eval({}), 1)
    def test_log_eval2(self):
        expr = Log(Variable("x"))
        self.assertAlmostEqual(expr.eval({"x": 3}), math.log(3))
    def test_log_eval3(self):
        expr = Log(Add(Constant(1), Variable("x")))
        self.assertAlmostEqual(expr.eval({"x": 3}), math.log(4))
    def test_log_diff1(self):
        expr = Log(Variable("x"))
        self.assertEqual(expr.diff("x"), Div(Constant(1), Variable("x")))
    def test_log_diff2(self):
        expr = Log(Add(Constant(1), Variable("x")))
        expected = Div(
            Add(Constant(0), Constant(1)),
            Add(Constant(1), Variable("x"))
        )
        self.assertEqual(expr.diff("x"), expected)
    def test_log_in_log_eval(self):
        expr = Log(Log(Variable("x")))
        self.assertEqual(expr.eval({"x": math.e}), 0)
    def test_log_in_log_diff(self):
        expr = Log(Log(Variable("x")))
        expected = Div(
            Div(Constant(1), Variable("x")),
            Log(Variable("x"))
            )
        self.assertEqual(expr.diff("x"), expected)
    def test_log_repr(self):
        expr = Log(Add(Constant(1), Variable("x")))
        self.assertEqual(expr.__repr__(), 'Log(Add(Constant(1), Variable("x")))')
    def test_log_str(self):
        expr = Log(Add(Constant(1), Variable("x")))
        self.assertEqual(expr.__str__(), "log((1 + x))")
    def test_log_eq(self):
        expr1 = Log(Add(Constant(1), Variable("x")))
        expr2 = Log(Add(Constant(1), Variable("x")))
        self.assertEqual(expr1, expr2)
    def test_log_neq(self):
        expr1 = Log(Add(Constant(1), Variable("x")))
        expr2 = Log(Add(Constant(1), Variable("y")))
        self.assertNotEqual(expr1, expr2)

    #test Pow
    def test_pow_eval1(self):
        expr = Pow(Constant(4), Constant(2))
        self.assertEqual(expr.eval({}), 16)
    def test_pow_eval2(self):
        expr = Pow(Variable("x"), Constant(2))
        self.assertEqual(expr.eval({"x": 3}), 9)
    def test_pow_eval3(self):
        expr = Pow(Variable("x"), Variable("x"))
        self.assertEqual(expr.eval({"x": 3}), 27)
    def test_pow_diff1(self):
        expr = Pow(Variable("x"), Constant(2))
        expected = Mul(
            Pow(Variable("x"), Constant(2)),
            Add(
                Div(
                    Mul(Constant(2), Constant(1)),
                    Variable("x")
                ),
                Mul(Constant(0), Log(Variable("x")))
            )
        )
        self.assertEqual(expr.diff("x"), expected)
    def test_pow_diff2(self):
        expr = Pow(Variable("x"), Variable("x"))
        expected = Mul(
            Pow(Variable("x"), Variable("x")),
            Add(
                Div(
                    Mul(Variable("x"), Constant(1)),
                    Variable("x")
                ),
                Mul(Constant(1), Log(Variable("x")))
            )
        )
        self.assertEqual(expr.diff("x"), expected)
    def test_pow_diff3(self):
        expr = Pow(
            Add(Variable("x"), Constant(1)),
            Add(Variable("x"), Constant(2))
        )
        expected = Mul(
            Pow(
                Add(Variable("x"), Constant(1)),
                Add(Variable("x"), Constant(2))
            ),
            Add(
                Div(
                    Mul(
                        Add(Variable("x"), Constant(2)),
                        Add(Constant(1), Constant(0))
                    ),
                    Add(Variable("x"), Constant(1))
                ),
                Mul(
                    Add(Constant(1), Constant(0)),
                    Log(
                        Add(Variable("x"), Constant(1))
                    )
                )
            )
        )
        self.assertEqual(expr.diff("x"), expected)
    def test_pow_diff4(self):
        expr = Pow(
            Mul(Constant(2), Variable("x")),
            Variable("x")
        )
        expected = Mul(
            Pow(
                Mul(Constant(2), Variable("x")),
                Variable("x")
            ),
            Add(
                Div(
                    Mul(
                        Variable("x"),
                        Add(
                            Mul(Constant(2), Constant(1)),
                            Mul(Constant(0), Variable("x"))
                        )
                    ),
                    Mul(Constant(2), Variable("x"))
                ),
                Mul(
                    Constant(1),
                    Log(
                        Mul(Constant(2), Variable("x"))
                    )
                )
            )
        )
        self.assertEqual(expr.diff("x"), expected)
    def test_pow_in_log_diff(self):
        expr = Log(Pow(Variable("x"), Constant(2)))
        expected = Div(
            Mul(
                Pow(Variable("x"), Constant(2)),
                Add(
                    Div(
                        Mul(Constant(2), Constant(1)),
                        Variable("x")
                    ),
                    Mul(
                        Constant(0),
                        Log(Variable("x"))
                    )
                )
            ),
            Pow(Variable("x"), Constant(2))
        )
        self.assertEqual(expr.diff("x"), expected)
    def test_pow_repr(self):
        expr = Pow(Variable("x"), Constant(2))
        self.assertEqual(expr.__repr__(), 'Pow(Variable("x"), Constant(2))')
    def test_pow_str(self):
        expr = Pow(Variable("x"), Constant(2))
        self.assertEqual(expr.__str__(), "(x ^ 2)")
    def test_pow_eq(self):
        expr1 = Pow(Variable("x"), Constant(2))
        expr2 = Pow(Variable("x"), Constant(2))
        self.assertEqual(expr1, expr2)
    def test_pow_neq(self):
        expr1 = Pow(Variable("x"), Constant(2))
        expr2 = Pow(Variable("x"), Constant(3))
        self.assertNotEqual(expr1, expr2)

    #test Sin
    def test_sin_eval1(self):
        expr = Sin(Constant(0))
        self.assertAlmostEqual(expr.eval({}), 0)
    def test_sin_eval2(self):
        expr = Sin(Variable("x"))
        self.assertAlmostEqual(expr.eval({"x": math.pi / 2}), 1)
    def test_sin_diff1(self):
        expr = Sin(Variable("x"))
        self.assertEqual(expr.diff("x"), Mul(Constant(1), Cos(Variable("x"))))
    def test_sin_diff2(self):
        expr = Sin(Mul(Constant(2), Variable("x")))
        expected = Mul(
            Add(
                Mul(Constant(2), Constant(1)),
                Mul(Constant(0), Variable("x"))
            ),
            Cos(
                Mul(Constant(2), Variable("x"))
            )
        )
        self.assertEqual(expr.diff("x"), expected)
    def test_sin_diff3(self):
        expr = Sin(Pow(Variable("x"), Constant(2)))
        expected = Mul(
            Mul(
                Pow(Variable("x"), Constant(2)),
                Add(
                    Div(
                        Mul(Constant(2), Constant(1)),
                        Variable("x")
                    ),
                    Mul(
                        Constant(0),
                        Log(Variable("x"))
                    )
                )
            ),
            Cos(
                Pow(Variable("x"), Constant(2))
            )
        )
        self.assertEqual(expr.diff("x"), expected)
    def test_sin_repr(self):
        expr = Sin(Variable("x"))
        self.assertEqual(expr.__repr__(), 'Sin(Variable("x"))')
    def test_sin_str(self):
        expr = Sin(Variable("x"))
        self.assertEqual(expr.__str__(), "sin(x)")
    def test_sin_eq(self):
        expr1 = Sin(Variable("x"))
        expr2 = Sin(Variable("x"))
        self.assertEqual(expr1, expr2)
    def test_sin_neq(self):
        expr1 = Sin(Variable("x"))
        expr2 = Sin(Variable("y"))
        self.assertNotEqual(expr1, expr2)

    #test Cos
    def test_cos_eval1(self):
        expr = Cos(Constant(0))
        self.assertAlmostEqual(expr.eval({}), 1)
    def test_cos_eval2(self):
        expr = Cos(Variable("x"))
        self.assertAlmostEqual(expr.eval({"x": math.pi / 2}), 0)
    def test_cos_diff1(self):
        expr = Cos(Variable("x"))
        expected = Mul(
            Constant(-1),
            Mul(Constant(1), Sin(Variable("x")))
        )
        self.assertEqual(expr.diff("x"), expected)
    def test_cos_diff2(self):
        expr = Cos(Mul(Constant(2), Variable("x")))
        expected = Mul(
            Constant(-1),
            Mul(
                Add(
                    Mul(Constant(2), Constant(1)),
                    Mul(Constant(0), Variable("x"))
                ),
                Sin(
                    Mul(Constant(2), Variable("x"))
                )
            )
        )
        self.assertEqual(expr.diff("x"), expected)
    def test_cos_diff3(self):
        expr = Cos(Pow(Variable("x"), Constant(2)))
        expected = Mul(
            Constant(-1),
            Mul(
                Mul(
                    Pow(Variable("x"), Constant(2)),
                    Add(
                        Div(
                            Mul(Constant(2), Constant(1)),
                            Variable("x")
                        ),
                        Mul(
                            Constant(0),
                            Log(Variable("x"))
                        )
                    )
                ),
                Sin(
                    Pow(Variable("x"), Constant(2))
                )
            )
        )
        self.assertEqual(expr.diff("x"), expected)
    def test_cos_repr(self):
        expr = Cos(Variable("x"))
        self.assertEqual(expr.__repr__(), 'Cos(Variable("x"))')
    def test_cos_str(self):
        expr = Cos(Variable("x"))
        self.assertEqual(expr.__str__(), "cos(x)")
    def test_cos_eq(self):
        expr1 = Cos(Variable("x"))
        expr2 = Cos(Variable("x"))
        self.assertEqual(expr1, expr2)
    def test_cos_neq(self):
        expr1 = Cos(Variable("x"))
        expr2 = Cos(Variable("y"))
        self.assertNotEqual(expr1, expr2)

    #test simplify
    def test_simplify_const(self):
        self.assertEqual(Constant(5).simplify(), Constant(5))
    def test_simplify_var(self):
        self.assertEqual(Variable("x").simplify(), Variable("x"))
    def test_simplify_add_zero(self):
        expr = Add(Constant(0), Variable("x"))
        self.assertEqual(expr.simplify(), Variable("x"))
    def test_simplify_add_constants(self):
        expr = Add(Constant(5), Constant(2))
        self.assertEqual(expr.simplify(), Constant(7))
    def test_simplify_add_no_simp(self):
        expr = Add(Variable("x"), Variable("y"))
        self.assertEqual(expr.simplify(), Add(Variable("x"), Variable("y")))
    def test_simplify_sub_zero(self):
        expr = Sub(Variable("x"), Constant(0))
        self.assertEqual(expr.simplify(), Variable("x"))
    def test_simplify_sub_constants(self):
        expr = Sub(Constant(5), Constant(2))
        self.assertEqual(expr.simplify(), Constant(3))
    def test_simplify_mul_zero(self):
        expr = Mul(Constant(0), Variable("x"))
        self.assertEqual(expr.simplify(), Constant(0))
    def test_simplify_mul_one(self):
        expr = Mul(Constant(1), Variable("x"))
        self.assertEqual(expr.simplify(), Variable("x"))
    def test_simplify_mul_constants(self):
        expr = Mul(Constant(5), Constant(2))
        self.assertEqual(expr.simplify(), Constant(10))
    def test_simplify_div_one(self):
        expr = Div(Variable("x"), Constant(1))
        self.assertEqual(expr.simplify(), Variable("x"))
    def test_simplify_div_constants(self):
        expr = Div(Constant(6), Constant(2))
        self.assertEqual(expr.simplify(), Constant(3))
    def test_simplify_div_zero_error(self):
        expr = Div(Variable("x"), Sub(Constant(2), Constant(2)))
        with self.assertRaises(ZeroDivisionError):
            expr.simplify()
    def test_simplify_pow_one(self):
        expr = Pow(Variable("x"), Constant(1))
        self.assertEqual(expr.simplify(), Variable("x"))
    def test_simplify_pow_zero(self):
        expr = Pow(Variable("x"), Constant(0))
        self.assertEqual(expr.simplify(), Constant(1))
    def test_simplify_pow_constants(self):
        expr = Pow(Constant(2), Constant(3))
        self.assertEqual(expr.simplify(), Constant(8))
    def test_simplify_sin_constant(self):
        expr = Sin(Constant(0))
        self.assertEqual(expr.simplify(), Constant(0))
    def test_simplify_cos_constant(self):
        expr = Cos(Constant(0))
        self.assertEqual(expr.simplify(), Constant(1))
    def test_simplify_log_constant(self):
        expr = Log(Constant(math.e))
        self.assertEqual(expr.simplify(), Constant(1))
    def test_simplify_nested(self):
        expr = Div(
            Mul(Constant(1), Constant(0)),
            Add(Constant(3), Constant(2))
        )
        self.assertEqual(expr.simplify(), Constant(0))
    def test_simplify_diff(self):
        expr = Mul(
            Add(Constant(3), Variable("x")),
            Add(Constant(2), Variable("x"))
        )
        expected = Add(
            Add(Constant(3), Variable("x")),
            Add(Constant(2), Variable("x"))
        )
        self.assertEqual(expr.diff("x").simplify(), expected)