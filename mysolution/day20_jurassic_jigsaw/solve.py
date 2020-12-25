from __future__ import annotations

import collections
import math
import os
import re
from collections.abc import Iterator, Sequence
from typing import NamedTuple, Optional

import more_itertools

Arrangement = tuple['Vec', 'Tile']

HEAD_RE = re.compile(r'Tile (?P<id>\d+):')


def main():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(this_dir, 'input.txt')
    tiles = read_input_files(input_file)

    # Part 1
    arrangements = arrange_tiles(tiles)
    corner_tile_ids = find_corner_tiles(arrangements)
    p1_answer = math.prod(corner_tile_ids)
    print(p1_answer)

    # Part 2
    grid = merge_tiles(arrangements)
    sea_monster_pixels = max(
        count_sea_monster_pixels(var_grid.area)
        for var_grid in grid.generate_variants()
    )
    sharps = sum(char == '#' for line in grid.area for char in line)
    p2_answer = sharps - sea_monster_pixels
    print(p2_answer)


class Vec(NamedTuple):
    row: int
    col: int

    def __pos__(self) -> Vec:
        return self

    def __neg__(self) -> Vec:
        return Vec(-self.row, -self.col)

    def __add__(self, other: Vec) -> Vec:
        return Vec(self.row + other.row, self.col + other.col)

    def __sub__(self, other: Vec) -> Vec:
        return self + (-other)


SEA_MONSTER_OFFSETS = [
    Vec(1, 0), Vec(2, 1),
    Vec(2, 4), Vec(1, 5), Vec(1, 6), Vec(2, 7),
    Vec(2, 10), Vec(1, 11), Vec(1, 12), Vec(2, 13),
    Vec(2, 16), Vec(1, 17), Vec(0, 18), Vec(1, 18), Vec(1, 19),
]


class Tile(NamedTuple):
    area: tuple[str, ...]

    def generate_variants(self) -> Iterator[Tile]:
        """
        Produces a sequence of all dihedral group (D2n) elements
        of this particular tile where n = 4.
        """
        tile = self
        yield tile
        yield tile.flip()
        for _ in range(3):
            tile = tile.rotate()
            yield tile
            yield tile.flip()

    def flip(self) -> Tile:
        """
        Returns a new tile but flipped at the vertical axis.
        """
        flipped_area = tuple(line[::-1] for line in self.area)
        return Tile(flipped_area)

    def rotate(self) -> Tile:
        """
        Returns a new tile rotated clockwise by 90 degrees.
        """
        rotated_area = tuple(''.join(chars) for chars in zip(*self.area[::-1]))
        return Tile(rotated_area)

    def erase_border(self) -> Tile:
        """
        Returns the tile without borders.
        """
        bare_area = tuple(line[1:-1] for line in self.area[1:-1])
        return Tile(bare_area)

    def touch(self, other: Tile) -> Optional[Vec]:
        """
        Finds where the other tile touches the main tile.
        Returns one of Pos(-1, 0), Pos(0, 1), Pos(1, 0), or Pos(0, -1).
        """
        if self.top == other.bot:
            return Vec(-1, 0)
        if self.rgt == other.lft:
            return Vec(0, 1)
        if self.bot == other.top:
            return Vec(1, 0)
        if self.lft == other.rgt:
            return Vec(0, -1)
        return None

    @property
    def top(self) -> str:
        """
        Top border reading left-to-right.
        """
        return self.area[0]

    @property
    def bot(self) -> str:
        """
        Bottom border reading left-to-right.
        """
        return self.area[-1]

    @property
    def lft(self) -> str:
        """
        Left border reading top-to-bottom.
        """
        return ''.join(line[0] for line in self.area)

    @property
    def rgt(self) -> str:
        """
        Right border reading top-to-bottom.
        """
        return ''.join(line[-1] for line in self.area)

    @classmethod
    def from_raw_body(cls, raw_body: list[str]) -> Tile:
        area = tuple(line.strip() for line in raw_body)
        return Tile(area)


def arrange_tiles(tiles: dict[int, Tile]) -> dict[int, Arrangement]:
    initial_id = more_itertools.first(tiles.keys())
    arrangements = {initial_id: (Vec(0, 0), tiles[initial_id])}
    queue = collections.deque([initial_id])

    while queue:
        current_id = queue.popleft()
        pos, arr = arrangements[current_id]
        for other_id, other_tile in tiles.items():
            if other_id in arrangements.keys():
                continue
            for other_arr in other_tile.generate_variants():
                if side := arr.touch(other_arr):
                    arrangements[other_id] = pos + side, other_arr
                    queue.append(other_id)
                    break

    return arrangements


def find_corner_tiles(arrangements: dict[int, Arrangement]) -> list[int]:
    lower = min(pos for pos, _ in arrangements.values())
    upper = max(pos for pos, _ in arrangements.values())
    corner_tiles = [
        id_ for id_, (pos, _) in arrangements.items()
        if pos.row in (lower.row, upper.row) and pos.col in (lower.col, upper.col)
    ]
    return corner_tiles


def merge_tiles(arrangements: dict[int, Arrangement]) -> Tile:
    lower = min(pos for pos, _ in arrangements.values())
    upper = max(pos for pos, _ in arrangements.values()) + Vec(1, 1)
    grid_map = {
        pos: arr.erase_border()
        for id_, (pos, arr) in arrangements.items()
    }

    grid_lines = []
    for row in range(lower.row, upper.row):
        row_tiles = [grid_map[row, col].area for col in range(lower.col, upper.col)]
        for line_fragments in zip(*row_tiles):
            grid_lines.append(''.join(line_fragments))

    return Tile(tuple(grid_lines))


def count_sea_monster_pixels(area: Sequence[str]) -> int:
    sea_monster_size = max(SEA_MONSTER_OFFSETS) + Vec(1, 1)
    sea_monster_pixels = set()

    for anchor_row in range(len(area) - sea_monster_size.row):
        for anchor_col in range(len(area[anchor_row]) - sea_monster_size.col):
            if all(area[anchor_row + offset.row][anchor_col + offset.col] == '#'
                   for offset in SEA_MONSTER_OFFSETS):
                sea_monster_pixels.update(
                    Vec(anchor_row + offset.row, anchor_col + offset.col)
                    for offset in SEA_MONSTER_OFFSETS
                )

    return len(sea_monster_pixels)


def read_input_files(input_file: str) -> dict[int, Tile]:
    """
    Extracts a dictionary mapping of input tile numbers to actual tiles.
    """
    with open(input_file) as input_fobj:
        tiles = {
            parse_raw_head(head.strip()): Tile.from_raw_body(body)
            for head, *body in more_itertools.split_at(input_fobj, lambda line: not line.strip())
        }
    return tiles


def parse_raw_head(raw_head: str) -> int:
    return int(HEAD_RE.fullmatch(raw_head).group('id'))


if __name__ == '__main__':
    main()
