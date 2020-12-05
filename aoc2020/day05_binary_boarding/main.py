from __future__ import annotations

import os
from dataclasses import dataclass

BINARY_TRANS = str.maketrans('FBLR', '0101')


def main():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(this_dir, 'input.txt')
    seats = read_input_files(input_file)

    # Part 1: print seat with largest id
    p1_answer = max(s.seat_id for s in seats)
    print(p1_answer)

    # Part 2: find missing seat
    p2_answer = find_missing_seat(seats)
    print(p2_answer)


@dataclass
class Seat:
    row: int
    col: int

    @property
    def seat_id(self):
        return self.row * 8 + self.col

    @classmethod
    def from_binary_partition(cls, code: str) -> Seat:
        code = code.translate(BINARY_TRANS)
        return Seat(row=int(code[:7], 2), col=int(code[7:], 2))


def find_missing_seat(seats: list[Seat]) -> int:
    """
    Find the missing seat in a cheating way
    by exploiting the cross-checking method (see problem statement).
    """
    min_id = min(s.seat_id for s in seats)
    max_id = max(s.seat_id for s in seats)
    answer = sum(range(min_id, max_id + 1)) - sum(s.seat_id for s in seats)
    return answer


def read_input_files(input_file: str) -> list[Seat]:
    """
    Extracts a list of valid passwords from the input file.
    """
    with open(input_file) as input_fobj:
        seats = [Seat.from_binary_partition(line.strip()) for line in input_fobj]
    return seats


if __name__ == '__main__':
    main()
