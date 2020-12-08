from __future__ import annotations

import os
import re
from collections.abc import Callable
from typing import Any

import more_itertools

SanitizeFunc = Callable[[str], Any]
PredicateFunc = Callable[[Any], bool]

PASSPORT_ATTRIBUTE_RULES = {
    'byr': re.compile(r'19[2-9][0-9]|200[0-2]'),
    'iyr': re.compile(r'201[0-9]|2020'),
    'eyr': re.compile(r'202[0-9]|2030'),
    'hgt': re.compile(r'(?:1[5-8][0-9]|19[0-3])cm|(?:59|6[0-9]|7[0-6])in'),
    'hcl': re.compile(r'#[0-9a-f]{6}'),
    'ecl': re.compile(r'amb|blu|brn|gry|grn|hzl|oth'),
    'pid': re.compile(r'[0-9]{9}'),
}


def main():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(this_dir, 'input.txt')
    passports = read_input_files(input_file)
    print(solve_p1(passports))
    print(solve_p2(passports))


def solve_p1(passports: list[dict]) -> int:
    """
    Count passports with required fields presented.
    """
    return sum(all_required_fields_present(p) for p in passports)


def solve_p2(passports: list[dict]) -> int:
    """
    Count passports with required fields presented and valid.
    """
    return sum(all_required_fields_valid(p) for p in passports)


def all_required_fields_present(passport: dict) -> bool:
    """
    Checks that all required attributes of a passport are present.
    """
    return PASSPORT_ATTRIBUTE_RULES.keys() <= passport.keys()


def all_required_fields_valid(passport: dict) -> bool:
    """
    Checks that all required attributes of a passport
    satisfy the corresponding regular expression.
    """
    return all(
        key in passport and pattern.fullmatch(passport[key])
        for key, pattern in PASSPORT_ATTRIBUTE_RULES.items()
    )


def read_input_files(input_file: str) -> list[dict]:
    """
    Extracts a list of valid passwords from the input file.
    """
    with open(input_file) as input_fobj:
        passports = [
            passport_attributes_from_chunk(chunk)
            for chunk in more_itertools.split_at(input_fobj, lambda line: not line.strip())
        ]
    return passports


def passport_attributes_from_chunk(chunk: list[str]) -> dict:
    """
    Creates a dictionary of passport attributes from the input chunk
    which is a list of lines (each line is the string content of such line).
    """
    attributes = {}
    for line in chunk:
        for pair in line.split():
            key, value = pair.split(':')
            attributes[key] = value
    return attributes


if __name__ == '__main__':
    main()
