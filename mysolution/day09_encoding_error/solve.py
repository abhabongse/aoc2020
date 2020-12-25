from __future__ import annotations

import collections
import os
from collections.abc import Sequence

import more_itertools


def main():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(this_dir, 'input.txt')
    numbers = read_input_files(input_file)

    # Part 1: find the first corruption in radio transmission
    p1_answer = find_first_corrupt(numbers, window_size=25)
    print(p1_answer)

    # Part 2: find the encryption weakness
    p2_answer = find_encryption_weakness(numbers, target=p1_answer)
    print(p2_answer)


def find_first_corrupt(numbers: list[int], window_size: int) -> int:
    """
    Finds the first corrupt number in O(nm log m) running time, where:
    - n: size of the input list of numbers
    - m: window size
    """
    for window_plus_one in more_itertools.windowed(numbers, window_size + 1):
        preceding_numbers = window_plus_one[:-1]
        target = window_plus_one[-1]
        if not pair_with_target_sum(preceding_numbers, target):
            return target
    raise RuntimeError('cannot find a candidate')


def pair_with_target_sum(numbers: Sequence[int], target: int) -> bool:
    """
    Determines whether there are two elements in the given list of numbers
    whose sum matches the given target.
    This function implements what is called two-pointers technique:
    1. Sort the list of numbers
    2. Consider a pair of points pointing to two numbers starting at each end of the list
    3. Move one of the pointers towards each other to adjust their sum to match the target
    """
    numbers = sorted(numbers)
    lo, hi = 0, len(numbers) - 1
    while lo < hi:
        if numbers[lo] + numbers[hi] < target:
            lo += 1
        elif numbers[lo] + numbers[hi] > target:
            hi -= 1
        else:
            return True
    return False


def find_encryption_weakness(numbers: list[int], target: int) -> int:
    """
    Finds the encryption weakness in O(n) running time
    where n is the size of the input list of numbers.
    """
    window = collections.deque()
    window_sum = 0
    for value in numbers:
        window.append(value)
        window_sum += value
        while window_sum > target:
            window_sum -= window.popleft()
        if len(window) >= 2 and window_sum == target:
            return min(window) + max(window)
    raise RuntimeError('cannot find a candidate')


def read_input_files(input_file: str) -> list[int]:
    """
    Extracts a list of numbers from the input file.
    """
    with open(input_file) as input_fobj:
        numbers = [int(line) for line in input_fobj]
    return numbers


if __name__ == '__main__':
    main()
