from __future__ import annotations

import os
import re
from collections.abc import Iterator
from dataclasses import dataclass, field

INSTR_RE = re.compile(r'(?P<name>\w+) (?P<arg>[-+]\d+)')


def main():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(this_dir, 'input.txt')
    program = read_input_files(input_file)

    # Part 1: find the accm value right before the first repeat of the same instruction
    runner = Runner(program)
    try:
        runner.run()
    except InfiniteLoop:
        pass
    p1_answer = runner.accm
    print(p1_answer)

    # Part 2: attempts to fix a single jmp <-> nop mutation and run program until the end
    p2_possible_answers = []
    for altered_program in generate_mutated_programs(program):
        runner = Runner(altered_program)
        try:
            runner.run()
        except InfiniteLoop:
            pass
        else:
            p2_possible_answers.append(runner.accm)
    print(p2_possible_answers)


@dataclass
class Instruction:
    name: str
    arg: int

    @classmethod
    def from_raw(cls, raw: str) -> Instruction:
        """
        Parses a line of instruction.
        """
        matchobj = INSTR_RE.fullmatch(raw)
        name = matchobj.group('name')
        arg = int(matchobj.group('arg'))
        return Instruction(name, arg)


@dataclass
class Runner:
    program: list[Instruction]
    pc: int = 0
    accm: int = 0
    visited: set[int] = field(default_factory=set)

    def run(self):
        while True:
            if self.pc in self.visited:
                raise InfiniteLoop
            self.visited.add(self.pc)
            previous_pc = self.pc
            self.execute_next()
            if previous_pc == len(self.program) - 1:
                break

    def execute_next(self):
        instr = self.program[self.pc]
        if instr.name == 'acc':
            self.accm += instr.arg
            self.pc += 1
        elif instr.name == 'jmp':
            self.pc += instr.arg
        elif instr.name == 'nop':
            self.pc += 1
        else:
            raise RuntimeError(f'unrecognized instruction: {instr}')


class InfiniteLoop(Exception):
    pass


def generate_mutated_programs(program: list[Instruction]) -> Iterator[list[Instruction]]:
    """
    Generates a sequence of programs (i.e. list of instructions)
    with a single mutation between jmp <-> nop instruction.
    """
    for index, instr in enumerate(program):
        if instr.name == 'jmp':
            altered_program = list(program)
            altered_program[index] = Instruction('nop', instr.arg)
            yield altered_program
        elif instr.name == 'nop':
            altered_program = list(program)
            altered_program[index] = Instruction('jmp', instr.arg)
            yield altered_program


def read_input_files(input_file: str) -> list[Instruction]:
    """
    Extracts a list of instructions (i.e. a program) from the input file.
    """
    with open(input_file) as input_fobj:
        program = [Instruction.from_raw(line.strip()) for line in input_fobj]
    return program


if __name__ == '__main__':
    main()
