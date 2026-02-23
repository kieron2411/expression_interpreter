import math
from enum import Enum
from expression import (
    Constant, Variable, 
    Add, Sub, Mul, Div,
    Log, Pow,
    Sin, Cos
)

"""
Supported syntax:
- numbers
- variables inside quotations (i.e. "x")
- constants (e, pi)
- functions (sin, cos, log)

Operator precedence:
1. ()
2. ^ (right associative i.e. x^y^z = x^(y^z))
3. * and / (left associative i.e. x/y*z = (x/y)*z)
4. + and - (left associative i.e. x+y-z = (x+y)-z)

Design choices:
- function arguments must be enclosed in parentheses
- multiplication must be written explicitly (i.e. 2*x not 2x)
- unary minus is interpreted as multiplication by -1
- unquoted identifiers are reserved words only (e, pi, sin, cos, log)
- numbers must begin with a digit (i.e. 0.5 not .5)
"""


class TokenType(Enum):
    NUMBER = 1
    VAR = 2
    IDENT = 3
    PLUS = 4
    MINUS = 5
    STAR = 6
    SLASH = 7
    CARET = 8
    LPAREN = 9
    RPAREN = 10
    EOF = 11

class Token:
    def __init__(self, type, value=None, position=None):
        self.type = type
        self.value = value
        self.position = position
    def __repr__(self):
        return f"Token({self.type}, {self.value}, {self.position})"
    def __eq__(self, other):
        return (isinstance(other, Token) and self.type == other.type 
        and self.value == other.value and self.position == other.position)
    
def to_tokens(text):
    tokens = []
    i = 0
    while i < len(text):
        if text[i].isspace():
            i += 1
            continue
        elif text[i] == "+":
            tokens.append(Token(TokenType.PLUS, None, i))
            i += 1
            continue
        elif text[i] == "-":
            tokens.append(Token(TokenType.MINUS, None, i))
            i += 1
            continue
        elif text[i] == "*":
            tokens.append(Token(TokenType.STAR, None, i))
            i += 1
            continue
        elif text[i] == "/":
            tokens.append(Token(TokenType.SLASH, None, i))
            i += 1
            continue
        elif text[i] == "^":
            tokens.append(Token(TokenType.CARET, None, i))
            i += 1
            continue
        elif text[i] == "(":
            tokens.append(Token(TokenType.LPAREN, None, i))
            i += 1
            continue
        elif text[i] == ")":
            tokens.append(Token(TokenType.RPAREN, None, i))
            i += 1
            continue
        elif text[i].isdigit():
            start_i = i
            seen_dot = False
            while i < len(text):
                if text[i].isdigit():
                    i += 1
                elif text[i] == ".":
                    if seen_dot:
                        raise SyntaxError(f"Second decimal point found at position {i}.")
                    else:
                        seen_dot = True
                        i += 1
                else:
                    break
            num = float(text[start_i : i])
            tokens.append(Token(TokenType.NUMBER, num, start_i))
            continue
        elif text[i].isalpha() or text[i] == "_":
            start_i = i
            while i < len(text):
                if text[i].isalpha() or text[i].isdigit() or text[i] == "_":
                    i += 1
                else:
                    break
            s = text[start_i : i]
            tokens.append(Token(TokenType.IDENT, s, start_i))
            continue
        elif text[i] == '"':
            start_i = i
            i += 1
            if i == len(text):
                raise SyntaxError(f"Unterminated variable starting at position {start_i}.")
            if text[i].isalpha() or text[i] == "_":
                while i < len(text):
                    if text[i].isalpha() or text[i].isdigit() or text[i] == "_":
                        i += 1
                    elif text[i] == '"':
                        i += 1
                        break
                    else:
                        raise SyntaxError(f"Invalid character in variable name at position {i}.")
                else:
                    raise SyntaxError(f"Unterminated variable starting at position {start_i}.")
                s = text[start_i + 1 : i - 1]
                tokens.append(Token(TokenType.VAR, s, start_i))
            else:
                raise SyntaxError(f"Invalid start of variable name at position {i}.")
        else:
            raise SyntaxError(f"Unknown character at position {i}.")
    tokens.append(Token(TokenType.EOF, None, i))
    return tokens

class ParserList:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0
    def current(self):
        return self.tokens[self.index]
    def advance(self):
        self.index += 1
    def expect(self, type):
        token = self.current()
        if token.type == type:
            self.advance()
            return token
        else:
            raise SyntaxError(f'Current token type "{token.type}" (position {token.position}) does not match expected type "{type}".')
    
    def parse_add_sub(self):
        left = self.parse_mul_div()
        while self.current().type in (TokenType.PLUS, TokenType.MINUS):
            op = self.current().type
            self.advance()
            right = self.parse_mul_div()
            if op == TokenType.PLUS:
                left = Add(left, right)
            else:
                left = Sub(left, right)
        return left
    def parse_mul_div(self):
        left = self.parse_minus()
        while self.current().type in (TokenType.STAR, TokenType.SLASH):
            op = self.current().type
            self.advance()
            right = self.parse_minus()
            if op == TokenType.STAR:
                left = Mul(left, right)
            else:
                left = Div(left, right)
        return left
    def parse_minus(self):
        if self.current().type == TokenType.MINUS:
            self.advance()
            expr = self.parse_minus()
            return Mul(Constant(-1), expr)
        else:
            return self.parse_pow()
    def parse_pow(self):
        base = self.parse_primary()
        if self.current().type == TokenType.CARET:
            self.advance()
            exp = self.parse_pow()
            base = Pow(base, exp)
        return base
    def parse_primary(self):
        token = self.current()
        if token.type == TokenType.NUMBER:
            self.advance()
            return Constant(token.value)
        elif token.type == TokenType.VAR:
            self.advance()
            return Variable(token.value)
        elif token.type == TokenType.IDENT:
            self.advance()
            if token.value == "pi":
                return Constant(math.pi)
            elif token.value == "e":
                return Constant(math.e)
            elif token.value == "sin":
                self.expect(TokenType.LPAREN)
                expr = self.parse_add_sub()
                self.expect(TokenType.RPAREN)
                return Sin(expr)
            elif token.value == "cos":
                self.expect(TokenType.LPAREN)
                expr = self.parse_add_sub()
                self.expect(TokenType.RPAREN)
                return Cos(expr)
            elif token.value == "log":
                self.expect(TokenType.LPAREN)
                expr = self.parse_add_sub()
                self.expect(TokenType.RPAREN)
                return Log(expr)
            else:
                raise SyntaxError(f'Unknown function/constant "{token.value}" at position {token.position}.')
        elif token.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_add_sub()
            self.expect(TokenType.RPAREN)
            return expr

        
def parse(text):
    tokens = to_tokens(text)
    parser_list = ParserList(tokens)
    expr = parser_list.parse_add_sub()
    parser_list.expect(TokenType.EOF)
    return expr
