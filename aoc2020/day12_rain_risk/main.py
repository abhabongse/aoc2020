from __future__ import annotations

import enum
import functools
import os
from typing import NamedTuple


def main():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(this_dir, 'input.txt')
    instructions = read_input_files(input_file)

    # Part 1
    final_state = functools.reduce(
        lambda curr, instr: curr.next_legacy_state(*instr),
        instructions, Ship(pos_x=0, pos_y=0, face_x=1, face_y=0),
    )
    p1_answer = abs(final_state.pos_x) + abs(final_state.pos_y)
    print(p1_answer)

    # Part 2
    final_state = functools.reduce(
        lambda curr, instr: curr.next_proper_state(*instr),
        instructions, Ship(pos_x=0, pos_y=0, face_x=10, face_y=1),
    )
    p2_answer = abs(final_state.pos_x) + abs(final_state.pos_y)
    print(p2_answer)


class Action(enum.Enum):
    MOVE_NORTH = 'N'
    MOVE_SOUTH = 'S'
    MOVE_EAST = 'E'
    MOVE_WEST = 'W'
    TURN_LEFT = 'L'
    TURN_RIGHT = 'R'
    MOVE_FORWARD = 'F'


class Ship(NamedTuple):
    pos_x: int
    pos_y: int
    face_x: int
    face_y: int

    def next_legacy_state(self, action: Action, value: int) -> Ship:
        if action == Action.MOVE_NORTH:
            return self._replace(pos_y=self.pos_y + value)
        elif action == Action.MOVE_SOUTH:
            return self._replace(pos_y=self.pos_y - value)
        elif action == Action.MOVE_EAST:
            return self._replace(pos_x=self.pos_x + value)
        elif action == Action.MOVE_WEST:
            return self._replace(pos_x=self.pos_x - value)
        elif action == Action.TURN_LEFT:
            return self.rotate_ccw(ticks=value // 90)
        elif action == Action.TURN_RIGHT:
            return self.rotate_cw(ticks=value // 90)
        elif action == Action.MOVE_FORWARD:
            return self._replace(
                pos_x=self.pos_x + self.face_x * value,
                pos_y=self.pos_y + self.face_y * value,
            )
        else:
            raise RuntimeError

    def next_proper_state(self, action: Action, value: int):
        if action == Action.MOVE_NORTH:
            return self._replace(face_y=self.face_y + value)
        elif action == Action.MOVE_SOUTH:
            return self._replace(face_y=self.face_y - value)
        elif action == Action.MOVE_EAST:
            return self._replace(face_x=self.face_x + value)
        elif action == Action.MOVE_WEST:
            return self._replace(face_x=self.face_x - value)
        elif action == Action.TURN_LEFT:
            return self.rotate_ccw(ticks=value // 90)
        elif action == Action.TURN_RIGHT:
            return self.rotate_cw(ticks=value // 90)
        elif action == Action.MOVE_FORWARD:
            return self._replace(
                pos_x=self.pos_x + self.face_x * value,
                pos_y=self.pos_y + self.face_y * value,
            )
        else:
            raise RuntimeError

    def rotate_ccw(self, ticks):
        return functools.reduce(lambda curr, _: curr.tick_ccw(), range(ticks), self)

    def tick_ccw(self):
        return self._replace(face_x=-self.face_y, face_y=self.face_x)

    def rotate_cw(self, ticks):
        return functools.reduce(lambda curr, _: curr.tick_cw(), range(ticks), self)

    def tick_cw(self):
        return self._replace(face_x=self.face_y, face_y=-self.face_x)


def read_input_files(input_file: str) -> list[tuple[Action, int]]:
    """
    Extracts a list of ship instructions.
    """
    with open(input_file) as input_fobj:
        instructions = [
            (Action(line[0]), int(line[1:]))
            for line in input_fobj
        ]
    return instructions


if __name__ == '__main__':
    main()
