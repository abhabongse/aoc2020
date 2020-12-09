from __future__ import annotations

import itertools
import os
import re
from collections.abc import Iterator

import more_itertools

INSTR_RE = re.compile(r'(?P<name>\w+) (?P<arg>[-+]\d+)')


def main():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(this_dir, 'input.txt')
    numbers = read_input_files(input_file)

    # Part 1: find the first corruption in radio transmission
    p1_answer = find_first_corrupt(numbers, preamble_size=25)
    print(p1_answer)

    # Part 2: find the encryption weakness
    p2_answer = find_encryption_weakness(numbers, target=p1_answer)
    print(p2_answer)


def find_first_corrupt(numbers: list[int], preamble_size: int) -> int:
    for index, value in enumerate(numbers[preamble_size:], start=preamble_size):
        preceding_numbers = numbers[index - preamble_size:index]
        sums_of_pairs = set(generate_sums_of_pairs(preceding_numbers))
        if value not in sums_of_pairs:
            return value
    raise RuntimeError('cannot find a candidate')


def find_encryption_weakness(numbers: list[int], target: int) -> int:
    for sublist in more_itertools.substrings(numbers):
        if len(sublist) >= 2 and sum(sublist) == target:
            return min(sublist) + max(sublist)
    raise RuntimeError('cannot find a candidate')


def generate_sums_of_pairs(numbers: list[int]) -> Iterator[int]:
    for x, y in itertools.combinations(numbers, r=2):
        yield x + y


def read_input_files(input_file: str) -> list[int]:
    """
    Extracts a list of numbers from the input file.
    """
    with open(input_file) as input_fobj:
        numbers = [int(line) for line in input_fobj]
    return numbers


if __name__ == '__main__':
    main()
