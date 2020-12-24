from __future__ import annotations

import collections
import functools
import itertools
import os
from collections.abc import Iterator, Set

IntTuple = tuple[int, ...]


def main():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(this_dir, 'input.txt')
    initial_pocket = read_input_files(input_file)

    # Part 1
    initial_pocket_3d = {c + (0,) for c in initial_pocket}
    result_pocket = functools.reduce(lambda p, _: expand_once(p), range(6), initial_pocket_3d)
    p1_answer = len(result_pocket)
    print(p1_answer)

    # Part 2
    initial_pocket_4d = {c + (0, 0) for c in initial_pocket}
    result_pocket = functools.reduce(lambda p, _: expand_once(p), range(6), initial_pocket_4d)
    p2_answer = len(result_pocket)
    print(p2_answer)


def expand_once(pocket: Set[IntTuple]) -> frozenset[IntTuple]:
    """
    Expands the current state of pocket
    (provided as a collection of active cube coordinates)
    into the next state according to the Conway-style rules.
    """
    active_neighbor_counts = collections.Counter(
        neighbor_coords
        for coords in pocket
        for neighbor_coords in generate_neighbors(coords)
    )
    next_pocket = frozenset(
        coords for coords, count in active_neighbor_counts.items()
        if coords in pocket and count == 2 or count == 3
    )
    return next_pocket


def generate_neighbors(coords: IntTuple) -> Iterator[IntTuple]:
    dim = len(coords)
    deltas = (-1, 0, 1)
    for shifts in itertools.product(deltas, repeat=dim):
        if all(s == 0 for s in shifts):
            continue
        shifted_coords = tuple(c + s for c, s in zip(coords, shifts))
        yield shifted_coords


def read_input_files(input_file: str) -> frozenset[IntTuple]:
    """
    Extracts an initial pocket dimension
    which is a set of active cube 3D coordinates.
    """
    with open(input_file) as input_fobj:
        pocket = frozenset(
            (x, y)
            for y, line in enumerate(input_fobj)
            for x, char in enumerate(line.strip())
            if char == '#'
        )
    return pocket


if __name__ == '__main__':
    main()
