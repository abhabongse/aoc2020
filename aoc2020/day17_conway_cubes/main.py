from __future__ import annotations

import functools
import os
from collections.abc import Iterator
from typing import Literal, NamedTuple


# TODO: Refactor multi-dimensional into one coherent function

def main():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(this_dir, 'input.txt')
    initial_pocket = read_input_files(input_file)

    # Part 1
    result_pocket = functools.reduce(lambda p, _: expand_once(p), range(6), initial_pocket)
    p1_answer = len(result_pocket)
    print(p1_answer)

    # Part 2
    initial_pocket_4d = set(Point4D(c.x, c.y, c.z, 0) for c in initial_pocket)
    result_pocket_4d = functools.reduce(lambda p, _: expand_once_4d(p), range(6), initial_pocket_4d)
    p2_answer = len(result_pocket_4d)
    print(p2_answer)


class Point3D(NamedTuple):
    x: int
    y: int
    z: int


class Point4D(NamedTuple):
    x: int
    y: int
    z: int
    w: int


class BoundAxis(NamedTuple):
    lower: int
    upper: int

    @classmethod
    def from_previous_pocket(cls, pocket: set[Point3D], axis: Literal['x', 'y', 'z']) -> BoundAxis:
        return BoundAxis(
            lower=min(getattr(c, axis) for c in pocket) - 1,
            upper=max(getattr(c, axis) for c in pocket) + 1,
        )

    @classmethod
    def from_previous_pocket_4d(cls, pocket: set[Point4D], axis: Literal['x', 'y', 'z', 'w']) -> BoundAxis:
        return BoundAxis(
            lower=min(getattr(c, axis) for c in pocket) - 1,
            upper=max(getattr(c, axis) for c in pocket) + 1,
        )


def expand_once(pocket: set[Point3D]) -> set[Point3D]:
    """
    Expands the current state of pocket into the next state
    according to the Conway-style rules.
    The pocket is a collection of active cube coordinates.
    """
    x_bound = BoundAxis.from_previous_pocket(pocket, 'x')
    y_bound = BoundAxis.from_previous_pocket(pocket, 'y')
    z_bound = BoundAxis.from_previous_pocket(pocket, 'z')

    next_pocket = set()
    for coord in generate_coords_within_bounds(x_bound, y_bound, z_bound):
        active_neighbors = sum(
            nbr_coord in pocket
            for nbr_coord in generate_neighbors(coord)
        )
        if (coord in pocket and active_neighbors in (2, 3)
                or coord not in pocket and active_neighbors == 3):
            next_pocket.add(coord)

    return next_pocket


def generate_coords_within_bounds(
        x_bound: BoundAxis,
        y_bound: BoundAxis,
        z_bound: BoundAxis,
) -> Iterator[Point3D]:
    for z in range(z_bound.lower, z_bound.upper + 1):
        for y in range(y_bound.lower, y_bound.upper + 1):
            for x in range(x_bound.lower, x_bound.upper + 1):
                yield Point3D(x, y, z)


def generate_neighbors(point: Point3D) -> Iterator[Point3D]:
    shifts = (-1, 0, 1)
    for dz in shifts:
        for dy in shifts:
            for dx in shifts:
                if dx != 0 or dy != 0 or dz != 0:
                    yield Point3D(point.x + dx, point.y + dy, point.z + dz)


def expand_once_4d(pocket: set[Point4D]) -> set[Point4D]:
    """
    Expands the current state of pocket into the next state
    according to the Conway-style rules.
    The pocket is a collection of active cube coordinates.
    """
    x_bound = BoundAxis.from_previous_pocket_4d(pocket, 'x')
    y_bound = BoundAxis.from_previous_pocket_4d(pocket, 'y')
    z_bound = BoundAxis.from_previous_pocket_4d(pocket, 'z')
    w_bound = BoundAxis.from_previous_pocket_4d(pocket, 'w')

    next_pocket = set()
    for coord in generate_coords_within_bounds_4d(x_bound, y_bound, z_bound, w_bound):
        active_neighbors = sum(
            nbr_coord in pocket
            for nbr_coord in generate_neighbors_4d(coord)
        )
        if (coord in pocket and active_neighbors in (2, 3)
                or coord not in pocket and active_neighbors == 3):
            next_pocket.add(coord)

    return next_pocket


def generate_coords_within_bounds_4d(
        x_bound: BoundAxis,
        y_bound: BoundAxis,
        z_bound: BoundAxis,
        w_bound: BoundAxis,
) -> Iterator[Point4D]:
    for w in range(w_bound.lower, w_bound.upper + 1):
        for z in range(z_bound.lower, z_bound.upper + 1):
            for y in range(y_bound.lower, y_bound.upper + 1):
                for x in range(x_bound.lower, x_bound.upper + 1):
                    yield Point4D(x, y, z, w)


def generate_neighbors_4d(point: Point4D) -> Iterator[Point4D]:
    shifts = (-1, 0, 1)
    for dw in shifts:
        for dz in shifts:
            for dy in shifts:
                for dx in shifts:
                    if dx != 0 or dy != 0 or dz != 0 or dw != 0:
                        yield Point4D(point.x + dx, point.y + dy, point.z + dz, point.w + dw)


def read_input_files(input_file: str) -> set[Point3D]:
    """
    Extracts an initial pocket dimension
    which is a set of active cube 3D coordinates.
    """
    with open(input_file) as input_fobj:
        initial_pocket = {
            Point3D(x, y, 0)
            for y, line in enumerate(input_fobj)
            for x, char in enumerate(line.strip())
            if char == '#'
        }
    return initial_pocket


if __name__ == '__main__':
    main()
