from __future__ import annotations

import functools
import operator
import os

import more_itertools


def main():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(this_dir, 'input.txt')
    surveys = read_input_files(input_file)
    print(solve_p1(surveys))
    print(solve_p2(surveys))


def solve_p1(surveys: list[list[str]]) -> int:
    """
    Count yes-answers across groups assuming that a group answers YES
    to a particular question if AT LEAST ONE person in the group does.
    """
    return sum(any_answering_yes(s) for s in surveys)


def solve_p2(surveys: list[list[str]]) -> int:
    """
    Count yes-answers across groups assuming that a group answers YES
    to a particular question if EVERY person unanimously answers YES.
    """
    return sum(all_answering_yes(s) for s in surveys)


def any_answering_yes(survey: list[str]) -> int:
    """
    Counts the number of A-Z questions where at least one person
    in the survey group answered yes.
    """
    set_union_op = operator.or_
    central_response = functools.reduce(set_union_op, (set(response) for response in survey))
    return len(central_response)


def all_answering_yes(survey: list[str]) -> int:
    """
    Counts the number of A-Z questions where every person
    in the survey group answered yes.
    """
    set_intersect_op = operator.and_
    central_response = functools.reduce(set_intersect_op, (set(response) for response in survey))
    return len(central_response)


def read_input_files(input_file: str) -> list[list[str]]:
    """
    Extracts a list of surveys from the input file.
    Each survey is returned as a list of individual response strings.
    The presence of a letter in the string indicates the yes-answer.
    """
    with open(input_file) as input_fobj:
        surveys = [
            [word.strip() for word in chunk]
            for chunk in more_itertools.split_at(input_fobj, lambda line: not line.strip())
        ]
    return surveys


if __name__ == '__main__':
    main()
