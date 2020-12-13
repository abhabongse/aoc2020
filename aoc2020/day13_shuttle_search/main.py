from __future__ import annotations

import itertools
import math
import os
from collections.abc import Iterator
from typing import Optional

Buses = list[Optional[int]]


def main():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(this_dir, 'input.txt')
    earliest_time, buses = read_input_files(input_file)

    # Part 1
    next_bus = next_bus_number_since(earliest_time, buses)
    p1_answer = next_bus * wait_time_until_next_bus(earliest_time, next_bus)
    print(p1_answer)

    # Part 2
    p2_answer = earliest_contest_event(buses)
    print(p2_answer)


def next_bus_number_since(earliest_time: int, buses: Buses):
    operating_buses = (b for b in buses if b is not None)
    next_bus = min(operating_buses, key=lambda b: wait_time_until_next_bus(earliest_time, b))
    return next_bus


def wait_time_until_next_bus(earliest_time: int, bus: int) -> int:
    return (-earliest_time) % bus


def earliest_contest_event(buses: Buses) -> int:
    """
    Computes the earliest timestamp T when the content happens.
    Specifically, for each bus B that has to depart from the bus stop
    at a delayed time D minutes after the timestamp T:

        T + D == 0  (mod B)

    In other words, T divided by B must yield a remainder in the same class as -D.
    This function does the following:
    - Extracts the preliminary chinese remainder theorem problem statement from the argument
    - Prepares the problem statement so that all moduli are relatively prime
    - Calls chinese remainder theorem algorithm to solve for answer
    """
    prelim_qr_pairs = [(b, -i) for i, b in enumerate(buses) if b is not None]
    max_q = max(q for q, _ in prelim_qr_pairs)

    qr_pairs = []
    for prime in generate_primes(limit=max_q):
        power = max(largest_power_factor(q, prime) for q, _ in prelim_qr_pairs)
        if power == 1:
            continue
        remainder = next(
            r % power for q, r in prelim_qr_pairs
            if q % power == 0
        )
        qr_pairs.append((power, remainder))

    return chinese_remainder(qr_pairs)


def generate_primes(*, limit: int = None) -> Iterator[int]:
    collected = []
    for value in itertools.count(2):
        if limit is not None and value > limit:
            return
        if all(value % p != 0 for p in collected):
            collected.append(value)
            yield value


def largest_power_factor(value: int, base: int) -> int:
    for count in itertools.count():
        if value % base != 0:
            return base ** count
        value //= base


def chinese_remainder(qr_pairs: list[tuple[int, int]]):
    prod = math.prod(q for q, _ in qr_pairs)
    result = sum(
        r * pow(prod // q, -1, q) * (prod // q)
        for q, r in qr_pairs
    )
    return result % prod


def read_input_files(input_file: str) -> tuple[int, Buses]:
    """
    Extracts an earliest bus boarding time and a list of bus numbers.bus_number
    Bus entry with 'x' will be returned as None.
    """
    with open(input_file) as input_fobj:
        earliest_time = int(next(input_fobj))
        buses = [
            parse_bus_number(token)
            for token in next(input_fobj).split(',')
        ]
    return earliest_time, buses


def parse_bus_number(token: str) -> Optional[int]:
    return None if token == 'x' else int(token)


if __name__ == '__main__':
    main()
