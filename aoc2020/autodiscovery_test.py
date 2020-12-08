from __future__ import annotations

import glob
import importlib.util
import os

import pytest

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def crawl_tests() -> list[pytest.mark.ParameterSet]:
    test_cases = [
        create_test(problem_dir, part_no, solution_file)
        for problem_dir in sorted(glob.glob(os.path.join(THIS_DIR, '*')))
        for part_no in [1, 2]
        for solution_file in glob.iglob(os.path.join(problem_dir, f'*.p{part_no}.sol'))
    ]
    return test_cases


def create_test(problem_dir: str, part_no: int, solution_file: str) -> pytest.mark.ParameterSet:
    problem_name = os.path.basename(problem_dir)
    solution_basename = os.path.relpath(solution_file, start=problem_dir)
    file_stem = solution_basename.removesuffix(f'.p{part_no}.sol')
    test_id = f'{problem_name}/{solution_basename}'
    return pytest.param(problem_name, file_stem, part_no, id=test_id)


@pytest.mark.parametrize("problem_name,file_stem,part_no", crawl_tests())
def test_from_file(problem_name: str, file_stem: str, part_no: int):
    problem_dir = os.path.join(THIS_DIR, problem_name)

    # Pre-load content of the solution file
    solution_file = os.path.join(problem_dir, f"{file_stem}.p{part_no}.sol")
    with open(solution_file) as fobj:
        solution = fobj.read().strip()

    # Load module and fetch relevant function to test
    program_file = os.path.join(problem_dir, 'main.py')
    spec = importlib.util.spec_from_file_location(problem_name, program_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    func = getattr(module, f"solve_p{part_no}")

    # Run the function with the input file and compare against solution
    input_file = os.path.join(problem_dir, f'{file_stem}.txt')
    answer = func(input_file)
    assert str(answer) == solution
