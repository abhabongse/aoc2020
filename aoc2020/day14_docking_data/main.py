from __future__ import annotations

import os
import re
from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import ClassVar, Literal, Pattern, get_type_hints


def main():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(this_dir, 'input.txt')
    operations = read_input_files(input_file)

    # Part 1
    program = Program(write_op_method='write_v1')
    for op in operations:
        program.execute(op)
    p1_answer = sum(program.memory.values())
    print(p1_answer)

    # Part 2
    program = Program(write_op_method='write_v2')
    for op in operations:
        program.execute(op)
    p2_answer = sum(program.memory.values())
    print(p2_answer)


@dataclass
class Program:
    """
    Represents a state of the program: current memory and mask.
    """
    write_op_method: Literal['write_v1', 'write_v2']
    memory: dict[int, int] = field(default_factory=dict)
    curr_mask: MaskOp = None

    def execute(self, op: BaseOp):
        """
        Executes the program based on the given base operation.
        """
        if isinstance(op, MaskOp):
            self.curr_mask = op
        elif isinstance(op, WriteOp):
            getattr(self, self.write_op_method)(op)
        else:
            raise RuntimeError

    def write_v1(self, write_op: WriteOp):
        bitmask = int(''.join('1' if b != 'X' else '0' for b in self.curr_mask.content), 2)
        content = int(''.join('1' if b == '1' else '0' for b in self.curr_mask.content), 2)
        self.memory[write_op.addr] = self.ternary_masking(bitmask, then_val=content, else_val=write_op.value)

    def write_v2(self, write_op: WriteOp):
        bitmask = int(''.join('1' if b != '0' else '0' for b in self.curr_mask.content), 2)
        for dyn_addr in self.generate_combinations(self.curr_mask.content):
            addr = self.ternary_masking(bitmask, then_val=dyn_addr, else_val=write_op.addr)
            self.memory[addr] = write_op.value

    @classmethod
    def generate_combinations(cls, bit_string: str) -> Iterator[int]:
        """
        Produces a sequence of all possible integers from the given `bit_string`
        where each 'X' can be replaced by either '0' or '1'.
        """
        if 'X' in bit_string:
            yield from cls.generate_combinations(bit_string.replace('X', '0', 1))
            yield from cls.generate_combinations(bit_string.replace('X', '1', 1))
        else:
            yield int(bit_string, 2)

    @classmethod
    def ternary_masking(cls, cond: int, then_val: int, else_val: int) -> int:
        """
        Computes an integer where each bit is taken from `then_val`
        if the corresponding bit (i.e. at the same location) in `cond` is 1;
        otherwise the bit value is taken from `else_val`.
        """
        inverted_cond = cond ^ ((1 << else_val.bit_length()) - 1)
        return cond & then_val | inverted_cond & else_val


@dataclass
class BaseOp:
    """
    Base class for all operations in the docking program.
    """
    subclasses: ClassVar[list[type[BaseOp]]] = []
    pattern: ClassVar[Pattern[str]]

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseOp.subclasses.append(cls)

    @classmethod
    def parse(cls, raw: str) -> BaseOp:
        """
        Parses an input raw string to an instance of `BaseOp` class.
        This method uses the compiled regexp associated to each subclass
        to determine which subclass whose instance should be constructed.
        It also uses the value extracted from regexp to populate the attributes.
        """
        for subclass in cls.subclasses:
            if matchobj := subclass.pattern.fullmatch(raw):
                type_hints = get_type_hints(subclass)
                data = {
                    k: type_hints[k](v) if k in type_hints else v
                    for k, v in matchobj.groupdict().items()
                }
                return subclass(**data)
        raise ValueError(f"unrecognized raw string: {raw}")


@dataclass
class MaskOp(BaseOp):
    pattern = re.compile(r'mask = (?P<content>[X01]{36})')
    content: str


@dataclass
class WriteOp(BaseOp):
    pattern = re.compile(r'mem\[(?P<addr>\d+)] = (?P<value>\d+)')
    addr: int
    value: int


def read_input_files(input_file: str) -> list[BaseOp]:
    """
    Extracts a list of operations to the docking program.
    """
    with open(input_file) as input_fobj:
        operations = [BaseOp.parse(line.strip()) for line in input_fobj]
    return operations


if __name__ == '__main__':
    main()
