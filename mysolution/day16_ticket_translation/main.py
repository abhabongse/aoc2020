from __future__ import annotations

import math
import os
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from typing import TypeVar, cast

import more_itertools

T = TypeVar('T')


def main():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(this_dir, 'input.txt')
    rules, my_ticket, nearby_tickets = read_input_files(input_file)

    # Part 1
    p1_answer = sum(sum(ticket_errors(tix, rules)) for tix in nearby_tickets)
    print(p1_answer)

    # Part 2
    nearby_tickets = [tix for tix in nearby_tickets if not ticket_errors(tix, rules)]
    matched_columns = resolve_attributes(rules, nearby_tickets)
    relevant_attrs = [
        my_ticket.attrs[mc]
        for mc, r in zip(matched_columns, rules)
        if r.name.startswith("departure")
    ]
    p2_answer = math.prod(relevant_attrs)
    print(p2_answer)


@dataclass
class Rule:
    name: str
    ranges: list[range]

    @classmethod
    def from_raw(cls, raw: str) -> Rule:
        name, raw_ranges = raw.split(": ")
        ranges = []
        for rg in raw_ranges.split(" or "):
            lower, upper = (int(token) for token in rg.split('-'))
            ranges.append(range(lower, upper + 1))
        return Rule(name, ranges)

    def __contains__(self, value: int) -> bool:
        return any(value in rg for rg in self.ranges)


@dataclass
class Ticket:
    attrs: list[int]

    @classmethod
    def from_raw(cls, raw: str) -> Ticket:
        attrs = [int(token) for token in raw.split(',')]
        return Ticket(attrs)


def ticket_errors(ticket: Ticket, rules: list[Rule]) -> list[int]:
    return [
        attr for attr in ticket.attrs
        if all(attr not in r for r in rules)
    ]


def resolve_attributes(rules: list[Rule], tickets: list[Ticket]) -> list[int]:
    # For each rule r at position r_index,
    # candidates[r_index] stores a list of column indices
    # where values of such column in all tickets satisfies the rule r
    candidate_sets = [
        {
            col for col, _ in enumerate(rules)
            if all(tix.attrs[col] in r for tix in tickets)
        }
        for r in rules
    ]

    # Assuming that the final solution is unique,
    # uses the process of elimination to match rules with columns
    matched_columns = [None for _ in rules]
    for _ in rules:
        index, cs = find_with_index(candidate_sets, lambda cs_: len(cs_) == 1)
        col = cs.pop()
        for other_cs in candidate_sets:
            other_cs.discard(col)
        matched_columns[index] = col

    assert all(isinstance(mc, int) for mc in matched_columns)
    return cast(list[int], matched_columns)


def find_with_index(iterable: Iterable[T], pred: Callable[[T], bool]) -> tuple[int, T]:
    for index, value in enumerate(iterable):
        if pred(value):
            return index, value
    raise ValueError("no value in the sequence satisfies the predicate")


def read_input_files(input_file: str) -> tuple[list[Rule], Ticket, list[Ticket]]:
    """
    Extracts a rules set, my own ticket, and a list of nearby tickets.
    """
    with open(input_file) as input_fobj:
        stripped_input = (line.strip() for line in input_fobj)
        rules, my_ticket, nearby_tickets = more_itertools.split_at(stripped_input, pred=lambda line: not line)
        rules = [Rule.from_raw(r) for r in rules]
        num_attrs = len(rules)

        assert len(my_ticket) == 2 and my_ticket[0].strip() == "your ticket:"
        my_ticket = Ticket.from_raw(my_ticket[1])
        assert len(my_ticket.attrs) == num_attrs

        assert len(nearby_tickets) >= 2 and nearby_tickets[0].strip() == "nearby tickets:"
        nearby_tickets = [Ticket.from_raw(t) for t in nearby_tickets[1:]]
        assert all(len(t.attrs) == num_attrs for t in nearby_tickets)

    return rules, my_ticket, nearby_tickets


if __name__ == '__main__':
    main()
