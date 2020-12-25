from __future__ import annotations

import contextlib
import itertools
import time
from collections.abc import Iterator

import more_itertools


def main():
    # starting_numbers = [0, 3, 6]
    start_numbers = [5, 2, 8, 16, 18, 0, 1]

    # Part 1
    target_pos = 2020
    with timer(message_prefix="timer: part 1 "):
        p1_answer = more_itertools.nth(speak_numbers(start_numbers), n=target_pos - 1)
    print(p1_answer)

    # Part 2
    target_pos = 30_000_000
    with timer(message_prefix="timer: part 2 "):
        p2_answer = more_itertools.nth(speak_numbers(start_numbers), n=target_pos - 1)
    print(p2_answer)


def speak_numbers(start_numbers: list[int]) -> Iterator[int]:
    """
    Produces an infinite sequence of spoken numbers in a game
    based on the given list of starting numbers.
    The implementation uses 0-indexing instead of 1-indexing.
    """
    assert start_numbers, "starting list cannot be empty"
    recent_indices = {}

    # Very first mandatory starting number
    value = start_numbers[0]
    yield value

    # Process remaining numbers
    for index, next_value in enumerate(start_numbers[1:], start=1):
        recent_indices[value] = index - 1
        value = next_value
        yield value

    # Calculate new numbers according to the rules
    for index in itertools.count(start=len(start_numbers)):
        next_value = (index - 1) - recent_indices.get(value, index - 1)
        recent_indices[value] = index - 1
        value = next_value
        yield value


@contextlib.contextmanager
def timer(message_prefix: str = ""):
    start_time = time.perf_counter()
    yield
    duration = time.perf_counter() - start_time
    print(f"{message_prefix}took {duration:.4f}s")


if __name__ == '__main__':
    main()
