from __future__ import annotations

import functools
import os
from collections.abc import Iterator


def main():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(this_dir, 'input.txt')
    area = read_input_files(input_file)

    # Part 1: count tress along sloped path
    p1_answer = count_trees_in_slope(area, dr=1, dc=3)
    print(p1_answer)

    # Part 2: product of tree counts along different slopes
    tree_counts = [
        count_trees_in_slope(area, dr=1, dc=1),
        count_trees_in_slope(area, dr=1, dc=3),
        count_trees_in_slope(area, dr=1, dc=5),
        count_trees_in_slope(area, dr=1, dc=7),
        count_trees_in_slope(area, dr=2, dc=1),
    ]
    p2_answer = functools.reduce(lambda x, y: x * y, tree_counts)
    print(tree_counts, p2_answer)


def count_trees_in_slope(area: list[str], dr: int, dc: int) -> int:
    """
    Counts the number of trees '#' along the sloped path described by (dr, dc)
    in the given area starting from the cell at (0, 0) until reaching beyond the last row.
    The area is assumed to be topologically horizontally wrapped around.
    """
    return sum(cell == '#' for cell in sample_in_slope(area, dr, dc))


def sample_in_slope(area: list[str], dr: int, dc: int) -> Iterator[str]:
    """
    Produces a sequence of cell contents along the sloped path described by (dr, dc)
    in the given area starting from the cell at (0, 0) until reaching beyond the last row.
    The area is assumed to be topologically horizontally wrapped around.
    """
    r = 0
    c = 0
    height = len(area)
    while r < height:
        width = len(area[r])
        yield area[r][c % width]
        r += dr
        c += dc


def read_input_files(input_file: str) -> list[str]:
    """
    Extracts a map area from the input file.
    The map area is a list of rows
    where each row is a string representation of that particular row.
    """
    with open(input_file) as input_fobj:
        area = [line.strip() for line in input_fobj]
    return area


if __name__ == '__main__':
    main()
