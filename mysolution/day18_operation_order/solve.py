from __future__ import annotations

import os

from lark import Lark, Transformer, v_args

ADD_MUL_EQ_GRAMMAR = '''
    ?expr: atom
         | expr "+" atom        -> add
         | expr "*" atom        -> mul

    ?atom: NUMBER               -> number
         | "(" expr ")"

    %import common.NUMBER
    %import common.WS_INLINE

    %ignore WS_INLINE
'''

ADD_B4_MUL_GRAMMAR = '''
    ?factor: term
           | factor "*" term    -> mul

    ?term: atom
         | term "+" atom        -> add

    ?atom: NUMBER               -> number
         | "(" factor ")"

    %import common.NUMBER
    %import common.WS_INLINE

    %ignore WS_INLINE
'''


@v_args(inline=True)
class TreeEvaluator(Transformer):
    def add(self, left, right):
        return left + right

    def mul(self, left, right):
        return left * right

    def number(self, value):
        return int(value)


def main():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(this_dir, 'input.txt')
    expressions = read_input_files(input_file)

    # Part 1
    add_mul_eq_parser = Lark(ADD_MUL_EQ_GRAMMAR, start='expr', parser='lalr', transformer=TreeEvaluator())
    p1_answer = sum(add_mul_eq_parser.parse(expr) for expr in expressions)
    print(p1_answer)

    # Part 2
    add_b4_mul_parser = Lark(ADD_B4_MUL_GRAMMAR, start='factor', parser='lalr', transformer=TreeEvaluator())
    p2_answer = sum(add_b4_mul_parser.parse(expr) for expr in expressions)
    print(p2_answer)


def read_input_files(input_file: str) -> list[str]:
    """
    Extracts a list of expressions.
    """
    with open(input_file) as input_fobj:
        expressions = [line.strip() for line in input_fobj]
    return expressions


if __name__ == '__main__':
    main()
