from __future__ import annotations

import os
import re

import more_itertools
from lark import Lark, LarkError

INT_RE = re.compile(r'(\d+)')

GRAMMAR_TEMPLATE = """
{body}

%import common.NUMBER
%import common.WS_INLINE

%ignore WS_INLINE
"""


def main():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(this_dir, 'input.txt')
    rules, messages = read_input_files(input_file)

    # Part 1
    parser = build_parser(rules, start=0)
    p1_answer = sum(validate(m, parser) for m in messages)
    print(p1_answer)

    # Part 2
    modified_rules = replace_rule(rules, "8: 42 | 42 8")
    modified_rules = replace_rule(modified_rules, "11: 42 31 | 42 11 31")
    parser = build_parser(modified_rules, start=0)
    p2_answer = sum(validate(m, parser) for m in messages)
    print(p2_answer)


def validate(text: str, parser: Lark) -> bool:
    try:
        parser.parse(text)
    except LarkError:
        return False
    else:
        return True


def build_parser(rules: list[str], start: int) -> Lark:
    grammar = '\n'.join(INT_RE.sub(r'rule\1', r) for r in rules)
    parser = Lark(grammar, start=f'rule{start}', parser='earley')
    return parser


def replace_rule(rules: list[str], new_rule: str) -> list[str]:
    rule_number, _ = new_rule.split(' ', maxsplit=1)
    rules = [
        new_rule if r.startswith(rule_number) else r
        for r in rules
    ]
    return rules


def read_input_files(input_file: str) -> tuple[list[str], list[str]]:
    """
    Extracts a grammar list.
    """
    with open(input_file) as input_fobj:
        rules, messages = more_itertools.split_at(input_fobj, lambda line: not line.strip())
        rules = [r.strip() for r in rules]
        messages = [m.strip() for m in messages]
    return rules, messages


if __name__ == '__main__':
    main()
