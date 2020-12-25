from __future__ import annotations

import itertools
from collections.abc import Iterator, Sequence

import more_itertools
from tqdm import trange

Arrows = dict[int, int]


def main():
    # arrangement = [3, 8, 9, 1, 2, 5, 4, 6, 7]
    arrangement = [4, 5, 9, 6, 7, 2, 8, 1, 3]

    # Part 1
    arrows = build_circular_arrows(arrangement)
    crab_modify_arrows(arrows, arrangement[0], plucks=3, repeat=100)

    final_arrangement = list(nodes_in_circle(arrows, start=1))
    p1_answer = ''.join(str(n) for n in final_arrangement[1:])
    print(p1_answer)

    # Part 2
    arrangement = arrangement + list(range(10, 1_000_001))
    arrows = build_circular_arrows(arrangement)
    crab_modify_arrows(arrows, arrangement[0], plucks=3, repeat=10_000_000)

    fst, snd, trd = more_itertools.take(3, nodes_in_circle(arrows, start=1))
    p2_answer = snd * trd
    print(p2_answer)


def build_circular_arrows(arrangement: Sequence[int]) -> Arrows:
    """
    Builds a circular graph as a dictionary mapping from one node label to the next.
    """
    looped_arrangement = itertools.chain(arrangement, arrangement[:1])
    arrows = {u: v for u, v in more_itertools.windowed(looped_arrangement, n=2)}
    return arrows


def nodes_in_circle(arrows: Arrows, start: int) -> Iterator[int]:
    """
    Obtains a sequence of node labels around the arrows graph
    starting from the given `start` label until it reaches back to start.
    """
    current = start
    while True:
        yield current
        current = arrows[current]
        if current == start:
            break


def crab_modify_arrows(arrows: Arrows, current: int, plucks: int, repeat: int = 1) -> int:
    """
    Modifies the arrows graph in-place according to crab's challenge
    starting at the given current node label.
    It returns the next *current* node label to resume the next step.
    """
    for _ in trange(repeat):
        plucked = more_itertools.take(plucks, nodes_in_circle(arrows, arrows[current]))
        candidates = count_in_modulus(current - 1, -1, modulo=len(arrows))
        dest = more_itertools.first_true(candidates, pred=lambda v: v not in plucked)
        rear = plucked[-1]
        arrows[current], arrows[rear], arrows[dest] = arrows[rear], arrows[dest], arrows[current]
        current = arrows[current]
    return current


def count_in_modulus(start: int, step: int = 1, *, modulo: int) -> Iterator[int]:
    """
    Produces an arithmetic sequence of numbers under the given modulus
    with 1-indexing (so remainder 0 would actually yield the modulus itself).
    """
    for value in itertools.count(start, step):
        yield value % modulo or modulo


if __name__ == '__main__':
    main()
