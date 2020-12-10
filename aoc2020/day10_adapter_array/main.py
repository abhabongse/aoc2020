from __future__ import annotations

import collections
import itertools
import os

import more_itertools


def main():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(this_dir, 'input.txt')
    adapters = read_input_files(input_file)

    # Part 1: adapter sanity check
    diff_counts = diff_counts_in_jolt_chain(adapters, gap=3)
    p1_answer = diff_counts[1] * diff_counts[3]
    print(p1_answer)

    # Part 2: count possible configurations
    p2_answer = count_valid_jolt_chains(adapters, gap=3)
    print(p2_answer)


def diff_counts_in_jolt_chain(adapters: list[int], gap: int) -> collections.Counter:
    """
    Counts the number of joltage differences between two consecutive power devices
    when all adapters are connected in chain from the charging outlet (0) to built-in adapter
    (assuming that the built-in adapter has the rating of the largest adapter plus gap).
    """
    builtin_adapter = max(adapters) + gap
    jolt_chain = itertools.chain([0], sorted(adapters), [builtin_adapter])
    diff_counts = collections.Counter(hi - lo for lo, hi in more_itertools.windowed(jolt_chain, 2))
    return diff_counts


def count_valid_jolt_chains(adapters: list[int], gap: int) -> int:
    """
    Count the number of configurations of functioning jolt chains
    from the charging outlet (0) to the built-in adapter
    (where two consecutive power devices must be within the given gap).

    This function implements a dynamic programming algorithm with O(nk) running time
    where n is the number of adapters and k is the input gap size.
    An improved version of this algorithm using O(n) time (not implemented here)
    is to maintain a sliding window of preceding config counts plus their total sum.
    """
    builtin_adapter = max(adapters) + gap
    jolt_chain = itertools.chain([0], sorted(adapters), [builtin_adapter])

    config_counts = collections.Counter({0: 1})
    for jolt in jolt_chain:
        for downstep in range(-gap, 0):
            config_counts[jolt] += config_counts[jolt + downstep]
    return config_counts[builtin_adapter]


def read_input_files(input_file: str) -> list[int]:
    """
    Extracts a list of adapter joltages.
    """
    with open(input_file) as input_fobj:
        adapters = [int(line) for line in input_fobj]
    return adapters


if __name__ == '__main__':
    main()
