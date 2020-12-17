from __future__ import annotations

import functools
import itertools
import os
from collections.abc import Iterator, Set

import more_itertools

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


def expand_once(pocket: Set[IntTuple]) -> set[IntTuple]:
    """
    Expands the current state of pocket
    (provided as a collection of active cube coordinates)
    into the next state according to the Conway-style rules.
    """
    next_pocket = set()
    for coords in generate_possible_cubes(pocket):
        active_neighbors = sum(
            neighbor_coords in pocket
            for neighbor_coords in generate_neighbors(coords)
        )
        if (coords in pocket and active_neighbors in (2, 3)
                or coords not in pocket and active_neighbors == 3):
            next_pocket.add(coords)
    return next_pocket


def generate_possible_cubes(pocket: Set[IntTuple]) -> Iterator[IntTuple]:
    dim = len(more_itertools.first(pocket))
    bounds = [
        range(min(coords[d] for coords in pocket) - 1,
              max(coords[d] for coords in pocket) + 2)
        for d in range(dim)
    ]
    yield from itertools.product(*bounds)


def generate_neighbors(coords: IntTuple) -> Iterator[IntTuple]:
    dim = len(coords)
    deltas = (-1, 0, 1)
    for shifts in itertools.product(deltas, repeat=dim):
        if all(s == 0 for s in shifts):
            continue
        shifted_coords = tuple(c + s for c, s in zip(coords, shifts))
        yield shifted_coords


def read_input_files(input_file: str) -> set[IntTuple]:
    """
    Extracts an initial pocket dimension
    which is a set of active cube 3D coordinates.
    """
    with open(input_file) as input_fobj:
        initial_pocket = {
            (x, y)
            for y, line in enumerate(input_fobj)
            for x, char in enumerate(line.strip())
            if char == '#'
        }
    return initial_pocket


if __name__ == '__main__':
    main()
