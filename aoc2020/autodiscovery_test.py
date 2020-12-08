from __future__ import annotations

import glob
import os
import runpy
from collections.abc import Iterator
from typing import Any

import pytest
import yaml

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def crawl_tests() -> list[pytest.mark.ParameterSet]:
    """
    Looks for tests.yaml file in each problem subdirectory
    and create a list of test cases base on its content.
    """
    tests = [
        test
        for test_config_file in sorted(glob.glob(os.path.join(THIS_DIR, '*', 'tests.yaml')))
        for test in extract_tests_from_config(test_config_file)
    ]
    return tests


def extract_tests_from_config(test_config_file: str) -> Iterator[pytest.mark.ParameterSet]:
    problem_dir = os.path.dirname(test_config_file)
    problem_name = os.path.basename(problem_dir)
    with open(test_config_file) as fobj:
        config = yaml.safe_load(fobj)
    program_file = os.path.join(problem_dir, config['program_file'])
    for test in config['tests']:
        input_file = os.path.join(problem_dir, test['input_file'])
        input_name = os.path.join(problem_name, test['input_file'])
        for part, solution in test['solutions'].items():
            try:
                solver = config['solvers'][part]
            except KeyError as exc:
                raise Exception(f'missing solver in config: {part}') from exc
            yield pytest.param(program_file, solver, input_file, solution, id=f"{input_name}::{part}")


@pytest.mark.parametrize("program_file,solver,input_file,solution", crawl_tests())
def test_from_file(program_file: str, solver: str, input_file: str, solution: Any):
    module = runpy.run_path(program_file)
    namespace = module | dict(input_file=input_file)
    answer = eval(solver, namespace)
    assert answer == solution
