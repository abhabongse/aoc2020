from __future__ import annotations

import functools
import itertools
import os


def main():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(this_dir, 'input.txt')
    expenses = read_input_files(input_file)

    # Part 1
    p1_answer = product_of_constrained_sum(expenses, target=2020, r=2)
    print(p1_answer)

    # Part 2
    p2_answer = product_of_constrained_sum(expenses, target=2020, r=3)
    print(p2_answer)


def product_of_constrained_sum(expenses: list[int], target: int, r: int = 2) -> int:
    """
    Finds the product of `r` numbers from within `expenses`
    whose sum exactly matches the given `target`.
    This implementation uses brute force approach with running time of degree-r polynomial.
    """
    for values in itertools.combinations(expenses, r=r):
        if sum(values) == target:
            return functools.reduce(lambda x, y: x * y, values)
    raise ValueError("no answer")


def read_input_files(input_file: str) -> list[int]:
    """
    Extracts a list of expenses from the input file.
    """
    with open(input_file) as input_fobj:
        expenses = [int(line) for line in input_fobj]
    return expenses


if __name__ == '__main__':
    main()
