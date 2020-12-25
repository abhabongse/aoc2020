from __future__ import annotations

import collections
import functools
import os
import re
from collections.abc import Sequence, Set
from typing import NamedTuple

DIRECTION_RE = re.compile(r'e|se|sw|w|nw|ne')


def main():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(this_dir, 'input.txt')
    navigations = read_input_files(input_file)

    # Part 1
    board = build_board(navigations)
    p1_answer = len(board)
    print(p1_answer)

    # Part 2
    final_board = functools.reduce(lambda b, _: flip_board(b), range(100), board)
    p2_answer = len(final_board)
    print(p2_answer)


class Vec(NamedTuple):
    x: int
    y: int

    def __add__(self, other: Vec) -> Vec:
        return Vec(self.x + other.x, self.y + other.y)


DIRECTIONAL_STEPS = {
    'e': Vec(1, 0),
    'se': Vec(1, -1),
    'sw': Vec(0, -1),
    'w': Vec(-1, 0),
    'nw': Vec(-1, 1),
    'ne': Vec(0, 1),
}


def build_board(navigations: Sequence[Sequence[str]]) -> frozenset[Vec]:
    counter = collections.Counter(displacement(n) for n in navigations)
    board = frozenset(k for k, v in counter.items() if v % 2 == 1)
    return board


def flip_board(board: Set[Vec]) -> frozenset[Vec]:
    neighbor_counts = collections.Counter(
        tile + move
        for tile in board
        for move in DIRECTIONAL_STEPS.values()
    )
    next_board = frozenset(
        tile for tile, count in neighbor_counts.items()
        if tile in board and count == 1 or count == 2
    )
    return next_board


def displacement(navigation: Sequence[str]) -> Vec:
    final_pos = sum((DIRECTIONAL_STEPS[d] for d in navigation), start=Vec(0, 0))
    return final_pos


def read_input_files(input_file: str) -> list[list[str]]:
    """
    Extracts a list of tile navigations
    where each navigation is a list of 6-way cardinal directions.
    """
    with open(input_file) as input_fobj:
        navigations = [DIRECTION_RE.findall(line.strip()) for line in input_fobj]
    return navigations


if __name__ == '__main__':
    main()
