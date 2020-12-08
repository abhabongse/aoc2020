from __future__ import annotations

import os
import re
from dataclasses import dataclass

PASSWD_RECORD_RE = re.compile(r'(?P<pol_fst>\d+)-(?P<pol_snd>\d+)\s+(?P<pol_letter>\w):\s+(?P<content>\w+)')


def main():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(this_dir, 'input.txt')
    records = read_input_files(input_file)
    print(solve_p1(records))
    print(solve_p2(records))


def solve_p1(records: list[PasswordRecord]) -> int:
    """
    Validates passwords under old policy.
    """
    return sum(r.is_valid_old for r in records)


def solve_p2(records: list[PasswordRecord]) -> int:
    """
    Validates passwords under new policy.
    """
    return sum(r.is_valid_new for r in records)


@dataclass
class PasswordRecord:
    pol_fst: int
    pol_snd: int
    pol_letter: str
    content: str

    @classmethod
    def parse(cls, text: str) -> PasswordRecord:
        match = PASSWD_RECORD_RE.fullmatch(text)
        return PasswordRecord(
            pol_fst=int(match.group('pol_fst')),
            pol_snd=int(match.group('pol_snd')),
            pol_letter=match.group('pol_letter'),
            content=match.group('content'),
        )

    @property
    def is_valid_old(self) -> int:
        """
        Whether the password `content` is valid under the **old** policy (part 1):
        the number of occurrences of `pol_letter` must be inclusively between
        `pol_fst` (lower bound) and `pol_snd` (upper bound).
        """
        lower_bound, upper_bound = self.pol_fst, self.pol_snd
        return lower_bound <= self.content.count(self.pol_letter) <= upper_bound

    @property
    def is_valid_new(self) -> int:
        """
        Whether the password `content` is valid under the **new** policy (part 2):
        at 1-indexing positions `pol_fst` and `pol_snd`,
        only exactly one of them must be the `pol_letter`.
        """
        fst_match = self.content[self.pol_fst - 1] == self.pol_letter
        snd_match = self.content[self.pol_snd - 1] == self.pol_letter
        return fst_match + snd_match == 1


def read_input_files(input_file: str) -> list[PasswordRecord]:
    """
    Extracts a list of password records from the input file.
    """
    with open(input_file) as input_fobj:
        records = [PasswordRecord.parse(line.strip()) for line in input_fobj]
    return records


if __name__ == '__main__':
    main()
