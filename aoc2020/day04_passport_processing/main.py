from __future__ import annotations

import os
import re
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from typing import Any

import more_itertools

SanitizeFunc = Callable[[str], Any]
PredicateFunc = Callable[[Any], bool]

HEIGHT_RE = re.compile(r'(\d+)(cm|in)')
HAIR_COLOR_RE = re.compile(r'#[0-9a-f]{6}')
EYE_COLOR_RE = re.compile(r'amb|blu|brn|gry|grn|hzl|oth')
PASSPORT_ID_RE = re.compile(r'[0-9]{9}')


def main():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(this_dir, 'input.txt')
    passports = read_input_files(input_file)

    # Part 1: count passports with required fields presented
    p1_answer = sum(p.all_fields_presented for p in passports)
    print(p1_answer)

    # Part 2: count passports with required fields valid
    p2_answer = sum(p.all_fields_valid for p in passports)
    print(p2_answer)


@dataclass
class Passport:
    """
    Passport data. All attributes are required except country id.
    """
    #: Birth Year
    byr: str = None
    #: Issue Year
    iyr: str = None
    #: Expiration Year
    eyr: str = None
    #: Height
    hgt: str = None
    #: Hair Color
    hcl: str = None
    #: Eye Color
    ecl: str = None
    #: Passport ID
    pid: str = None
    #: Country ID
    cid: str = None

    @property
    def all_fields_presented(self):
        """
        Checks that all required fields are presented.
        """
        return (self.byr is not None
                and self.iyr is not None
                and self.eyr is not None
                and self.hgt is not None
                and self.hcl is not None
                and self.ecl is not None
                and self.pid is not None)

    @property
    def all_fields_valid(self):
        """
        Checks that all required fields are valid.
        Note: could have used some data validation library, but kinda lazy now.
        """
        if not self.all_fields_presented:
            return False
        results = [
            self._validate_standard(self.byr, sanitize=int, predicate=lambda x: 1920 <= x <= 2002),
            self._validate_standard(self.iyr, sanitize=int, predicate=lambda x: 2010 <= x <= 2020),
            self._validate_standard(self.eyr, sanitize=int, predicate=lambda x: 2020 <= x <= 2030),
            self._validate_height(self.hgt),
            HAIR_COLOR_RE.fullmatch(self.hcl),
            EYE_COLOR_RE.fullmatch(self.ecl),
            PASSPORT_ID_RE.fullmatch(self.pid),
        ]
        return all(results)

    @classmethod
    def _validate_standard(cls, value: str, sanitize: SanitizeFunc = None, predicate: PredicateFunc = None) -> bool:
        if sanitize:
            try:
                value = sanitize(value)
            except ValueError:
                return False
        if predicate:
            return predicate(value)
        return True

    @classmethod
    def _validate_height(cls, value: str) -> bool:
        if matchobj := HEIGHT_RE.fullmatch(value):
            num, unit = matchobj.groups()
            if unit == 'cm' and 150 <= int(num) <= 193 or unit == 'in' and 59 <= int(num) <= 76:
                return True
        return False

    @classmethod
    def from_attribute_pairs(cls, attribute_pairs: Iterator[str]) -> Passport:
        data = {}
        for pair in attribute_pairs:
            key, value = pair.split(':')
            data[key] = value
        return Passport(**data)


def read_input_files(input_file: str) -> list[Passport]:
    """
    Extracts a list of valid passwords from the input file.
    """
    with open(input_file) as input_fobj:
        passports = [
            Passport.from_attribute_pairs(pair for line in batch for pair in line.split())
            for batch in more_itertools.split_at(input_fobj, lambda line: not line.strip())
        ]
    return passports


if __name__ == '__main__':
    main()
