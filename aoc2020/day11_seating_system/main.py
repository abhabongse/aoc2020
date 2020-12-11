from __future__ import annotations

import enum
import itertools
import os
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal, Optional

TraceMode = Literal['adjacent', 'visible']


def main():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(this_dir, 'input.txt')
    seatmap = read_input_files(input_file)

    # Part 1
    stable_seatmap_by_adjacency = repeat_until_stable(seatmap, trace='adjacent')
    p1_answer = sum(s == Seat.OCCUPIED for s in stable_seatmap_by_adjacency.area.values())
    print(p1_answer)

    # Part 2
    stable_seatmap_by_visibility = repeat_until_stable(seatmap, trace='visible')
    p2_answer = sum(s == Seat.OCCUPIED for s in stable_seatmap_by_visibility.area.values())
    print(p2_answer)


def repeat_until_stable(seatmap: SeatMap, trace: TraceMode) -> SeatMap:
    for _ in itertools.count(start=1):
        prev_seatmap, seatmap = seatmap, seatmap.next_round(trace)
        if seatmap == prev_seatmap:
            return seatmap


class Seat(enum.Enum):
    FLOOR = '.'
    EMPTY = 'L'
    OCCUPIED = '#'

    def next_state(self, traced_seats: Sequence[Seat], tolerance: int) -> Seat:
        """
        Compute the next seat state according to the following rules:
        - If a seat is EMPTY and there are no OCCUPIED seats in trace seats,
          the seat becomes OCCUPIED.
        - If a seat is OCCUPIED and four or more traced seats are also OCCUPIED,
          the seat becomes EMPTY.
        - Otherwise, the seat's state does not change.
        """
        if self == Seat.EMPTY and all(s != Seat.OCCUPIED for s in traced_seats):
            return Seat.OCCUPIED
        elif self == Seat.OCCUPIED and sum(s == Seat.OCCUPIED for s in traced_seats) >= tolerance:
            return Seat.EMPTY
        else:
            return self


@dataclass
class SeatMap:
    row_size: int
    col_size: int
    area: dict[tuple[int, int], Seat]

    def __repr__(self):
        builder = []
        for r in range(self.row_size):
            for c in range(self.col_size):
                builder.append(self.area[r, c].value)
            builder.append('\n')
        return ''.join(builder)

    @classmethod
    def from_raw_area(cls, area: list[str]) -> SeatMap:
        row_size = len(area)
        col_size = len(area[0])
        assert all(len(line) == col_size for line in area)
        area = {
            (r, c): Seat(char)
            for r, line in enumerate(area)
            for c, char in enumerate(line)
        }
        return SeatMap(row_size, col_size, area)

    def next_round(self, trace: TraceMode) -> SeatMap:
        """
        Obtains the next seatmap state.
        """
        if trace == 'adjacent':
            trace_func = self.trace_adjacent
            tolerance = 4
        elif trace == 'visible':
            trace_func = self.trace_visible
            tolerance = 5
        else:
            raise RuntimeError(f"unknown trace mode {trace!r}")

        next_area = {}
        for r in range(self.row_size):
            for c in range(self.col_size):
                traced_seats = [
                    trace_func(r, c, dr, dc)
                    for dr in [-1, 0, +1]
                    for dc in [-1, 0, +1]
                ]
                next_area[r, c] = self.area[r, c].next_state(traced_seats, tolerance)
        return SeatMap(self.row_size, self.col_size, next_area)

    def trace_adjacent(self, center_r: int, center_c: int, diff_r: int, diff_c: int) -> Optional[Seat]:
        if diff_r == 0 and diff_c == 0:
            return None
        r = center_r + diff_r
        c = center_c + diff_c
        if 0 <= r < self.row_size and 0 <= c < self.col_size:
            return self.area[r, c]
        return None

    def trace_visible(self, center_r: int, center_c: int, diff_r: int, diff_c: int) -> Optional[Seat]:
        if diff_r == 0 and diff_c == 0:
            return None
        r = center_r + diff_r
        c = center_c + diff_c
        while 0 <= r < self.row_size and 0 <= c < self.col_size:
            if self.area[r, c] in (Seat.EMPTY, Seat.OCCUPIED):
                return self.area[r, c]
            r += diff_r
            c += diff_c
        return None


def read_input_files(input_file: str) -> SeatMap:
    """
    Extracts a seating map.
    """
    with open(input_file) as input_fobj:
        area = [[Seat(char) for char in line.strip()] for line in input_fobj]
    return SeatMap.from_raw_area(area)


if __name__ == '__main__':
    main()
