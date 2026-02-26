#!/usr/bin/env python3

import argparse
import sys
from parser import parse

def main():
    parser = argparse.ArgumentParser(
    description="Symbolic expression CLI",
    epilog="""
Expression syntax:
  - Variables must be quoted: "x"
  - Operators: +  -  *  /  ^
  - Functions: sin(...), cos(...), log(...)
  - Constants: pi, e

Examples:
  eval '2*"x" + 3' --set x=4
  diff 'sin("x")' --var x

Chaining commands:
  diff 'sin("x")^2' --var x | simplify
  diff 'sin("x")' --var x | eval --set x=1.2
""",
    formatter_class=argparse.RawDescriptionHelpFormatter
)

    subparsers = parser.add_subparsers(dest="command", required=True)

    eval_parser = subparsers.add_parser("eval", help="Evaluate an expression")
    eval_parser.add_argument("expr", nargs="?", help="Expression string")
    eval_parser.add_argument("--set", action="append", default=[], help="Variable assignment in the form x=3")

    diff_parser = subparsers.add_parser("diff", help="Differentiate an expression")
    diff_parser.add_argument("expr", nargs="?", help="Expression string")
    diff_parser.add_argument("--var", required=True, help="Variable to differentiate with respect to")

    simp_parser = subparsers.add_parser("simplify", help="Simplify an expression")
    simp_parser.add_argument("expr", nargs="?", help="Expression string")

    args = parser.parse_args()

    if args.expr is not None:
        expr_text = args.expr
    else:
        expr_text = sys.stdin.read().strip()
    if not expr_text:
        parser.error("No expression provided")

    try:
        if args.command == "eval":
            env = {}
            for pair in args.set:
                temp = pair.split("=", 1)
                env[temp[0]] = float(temp[1])
            parsed_expr = parse(expr_text)
            print(parsed_expr.eval(env))
            return 0
        
        elif args.command == "diff":
            parsed_expr = parse(expr_text)
            print(parsed_expr.diff(args.var))
            return 0

        elif args.command == "simplify":
            parsed_expr = parse(expr_text)
            print(parsed_expr.simplify())
            return 0
    
    except (SyntaxError, ValueError, ZeroDivisionError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise(SystemExit(main()))