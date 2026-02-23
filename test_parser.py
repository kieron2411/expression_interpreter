import unittest
import math
from parser import (
    TokenType, Token, to_tokens, parse
)
from expression import (
    Constant, Variable, 
    Add, Sub, Mul, Div,
    Log, Pow,
    Sin, Cos
)

class TestParser(unittest.TestCase):
    #test conversion to tokens
    def test_to_tokens1(self):
        s = '2 + 3'
        expected = [
            Token(TokenType.NUMBER, 2.0, 0),
            Token(TokenType.PLUS, None, 2),
            Token(TokenType.NUMBER, 3.0, 4),
            Token(TokenType.EOF, None, 5)
        ]
        self.assertEqual(to_tokens(s), expected)
    def test_to_tokens2(self):
        s = '2.5 * "x"'
        expected = [
            Token(TokenType.NUMBER, 2.5, 0),
            Token(TokenType.STAR, None, 4),
            Token(TokenType.VAR, "x", 6),
            Token(TokenType.EOF, None, 9)
        ]
        self.assertEqual(to_tokens(s), expected)
    def test_to_tokens3(self):
        s = '"var_1" / cos(pi)'
        expected = [
            Token(TokenType.VAR, "var_1", 0),
            Token(TokenType.SLASH, None, 8),
            Token(TokenType.IDENT, "cos", 10),
            Token(TokenType.LPAREN, None, 13),
            Token(TokenType.IDENT, "pi", 14),
            Token(TokenType.RPAREN, None, 16),
            Token(TokenType.EOF, None, 17)
        ]
        self.assertEqual(to_tokens(s), expected)
    def test_to_tokens4(self):
        s = '"x"^2 + "y"^2'
        expected = [
            Token(TokenType.VAR, "x", 0),
            Token(TokenType.CARET, None, 3),
            Token(TokenType.NUMBER, 2.0, 4),
            Token(TokenType.PLUS, None, 6),
            Token(TokenType.VAR, "y", 8),
            Token(TokenType.CARET, None, 11),
            Token(TokenType.NUMBER, 2.0, 12),
            Token(TokenType.EOF, None, 13)
        ]
        self.assertEqual(to_tokens(s), expected)
    def test_to_tokens_error1(self):
        s = '5 & 3'
        with self.assertRaises(SyntaxError) as context:
            to_tokens(s)
        self.assertEqual(str(context.exception), "Unknown character at position 2.")
    def test_to_tokens_error2(self):
        s = '"1var"'
        with self.assertRaises(SyntaxError) as context:
            to_tokens(s)
        self.assertEqual(str(context.exception), "Invalid start of variable name at position 1.")
    def test_to_tokens_error3(self):
        s = '"var'
        with self.assertRaises(SyntaxError) as context:
            to_tokens(s)
        self.assertEqual(str(context.exception), "Unterminated variable starting at position 0.")

    #test conversion to Expr tree
    def test_parse1(self):
        s = '2 + 3'
        self.assertEqual(parse(s), Add(Constant(2), Constant(3)))
    def test_parse2(self):
        s = '2.5 * "x"'
        self.assertEqual(parse(s), Mul(Constant(2.5), Variable("x")))
    def test_parse3(self):
        s = '"var_1" / cos(pi)'
        expected = Div(
            Variable("var_1"),
            Cos(Constant(math.pi))
        )
        self.assertEqual(parse(s), expected)
    def test_parse4(self):
        s = '"x"^2 + "y"^2'
        expected = Add(
            Pow(Variable("x"), Constant(2)),
            Pow(Variable("y"), Constant(2))
        )
        self.assertEqual(parse(s), expected)
    def test_parse_precedence1(self):
        s = '2 + 3 * "x"'
        expected = Add(
            Constant(2),
            Mul(Constant(3), Variable("x"))
        )
        self.assertEqual(parse(s), expected)
    def test_parse_precedence2(self):
        s = '2 * "x" + 3'
        expected = Add(
            Mul(Constant(2), Variable("x")),
            Constant(3)
        )
        self.assertEqual(parse(s), expected)
    def test_parse_precedence3(self):
        s = '-"x"^2 * (3 + "y")'
        expected = Mul(
            Mul(
                Constant(-1),
                Pow(Variable("x"), Constant(2))
            ),
            Add(Constant(3), Variable("y"))
        )
        self.assertEqual(parse(s), expected)
    def test_parse_associativity1(self):
        s = '"x" / "y" * "z"'
        expected = Mul(
            Div(Variable("x"), Variable("y")),
            Variable("z")
        )
        self.assertEqual(parse(s), expected)
    def test_parse_associativity2(self):
        s = '"x"^"y"^2'
        expected = Pow(
            Variable("x"),
            Pow(Variable("y"), Constant(2))
        )
        self.assertEqual(parse(s), expected)
    
    #test parsed expression works
    def test_parse_eval(self):
        s = '5 + "x" * 4'
        self.assertEqual(parse(s).eval({"x": 3}), 17)
    def test_parse_diff(self):
        s = 'cos("x") + 3'
        expected = Add(
            Mul(
                Constant(-1),
                Mul(Constant(1), Sin(Variable("x")))
            ),
            Constant(0)
        )
        self.assertEqual(parse(s).diff("x"), expected)
    def test_parse_diff_simplify(self):
        s = 'sin("x")'
        self.assertEqual(parse(s).diff("x").simplify(), Cos(Variable("x")))

    #test parse errors
    def test_parse_error1(self):
        s = 'x + 1'
        with self.assertRaises(SyntaxError) as context:
            parse(s)
        self.assertEqual(str(context.exception), 'Unknown function/constant "x" at position 0.')
    def test_parse_error2(self):
        s = '2 + 3)'
        with self.assertRaises(SyntaxError) as context:
            parse(s)
        self.assertEqual(str(context.exception), 'Current token type "TokenType.RPAREN" (position 5) does not match expected type "TokenType.EOF".')
