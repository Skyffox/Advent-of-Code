# pylint: disable=line-too-long, missing-function-docstring, multiple-statements
"""
Day 16: Chronal Classification

Part 1: Ignoring the opcode numbers, how many samples in your puzzle input behave like three or more opcodes?
Answer: 607

Part 2: What value is contained in register 0 after executing the test program?
Answer: 577
"""

from typing import List, Dict, Callable, Tuple
import re
from copy import deepcopy
from utils import profiler


def get_input(file_path: str) -> List[str]:
    """
    Reads the input file and returns a list of stripped lines.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        list[str]: A list of lines with leading/trailing whitespace removed.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file.readlines()]


def parse_input(data: List[str]) -> Tuple[List[Tuple[List[int], List[int], List[int]]], List[List[int]]]:
    """
    Parses the raw input lines into two parts:
      - Samples with before/after register states and instructions.
      - A program consisting of opcode instructions.

    Args:
        data (List[str]): The raw input data.

    Returns:
        Tuple[List[Tuple], List[List[int]]]: Parsed samples and program.
    """
    samples = []
    i = 0
    while i < len(data):
        if data[i].startswith("Before"):
            # Parse one sample consisting of before, instruction, and after
            before = list(map(int, re.findall(r"\d+", data[i])))
            instr = list(map(int, data[i + 1].split()))
            after = list(map(int, re.findall(r"\d+", data[i + 2])))
            samples.append((before, instr, after))
            i += 3
        elif data[i] == "":
            i += 1
        else:
            break

    # The rest of the input is the actual test program
    program = [list(map(int, line.split())) for line in data[i:] if line]
    return samples, program


# Define all 16 possible opcodes
def addr(r, a, b, c): r[c] = r[a] + r[b]
def addi(r, a, b, c): r[c] = r[a] + b
def mulr(r, a, b, c): r[c] = r[a] * r[b]
def muli(r, a, b, c): r[c] = r[a] * b
def banr(r, a, b, c): r[c] = r[a] & r[b]
def bani(r, a, b, c): r[c] = r[a] & b
def borr(r, a, b, c): r[c] = r[a] | r[b]
def bori(r, a, b, c): r[c] = r[a] | b
def setr(r, a, _, c): r[c] = r[a]
def seti(r, a, _, c): r[c] = a
def gtir(r, a, b, c): r[c] = 1 if a > r[b] else 0
def gtri(r, a, b, c): r[c] = 1 if r[a] > b else 0
def gtrr(r, a, b, c): r[c] = 1 if r[a] > r[b] else 0
def eqir(r, a, b, c): r[c] = 1 if a == r[b] else 0
def eqri(r, a, b, c): r[c] = 1 if r[a] == b else 0
def eqrr(r, a, b, c): r[c] = 1 if r[a] == r[b] else 0

# Map all operation names to their corresponding functions
ALL_OPS: Dict[str, Callable[[List[int], int, int, int], None]] = {
    "addr": addr, "addi": addi, "mulr": mulr, "muli": muli,
    "banr": banr, "bani": bani, "borr": borr, "bori": bori,
    "setr": setr, "seti": seti, "gtir": gtir, "gtri": gtri,
    "gtrr": gtrr, "eqir": eqir, "eqri": eqri, "eqrr": eqrr
}


@profiler
def part_one(data_input: List[str]) -> int:
    """
    Counts how many samples match three or more opcodes.

    Args:
        data_input (List[str]): Raw input lines.

    Returns:
        int: Number of samples that behave like three or more opcodes.
    """
    samples, _ = parse_input(data_input)
    count = 0

    for before, instr, after in samples:
        matches = 0
        for func in ALL_OPS.values():
            regs = deepcopy(before)
            func(regs, *instr[1:])  # Apply the function using instruction parameters (a, b, c)
            if regs == after:
                matches += 1
        if matches >= 3:
            count += 1

    return count


@profiler
def part_two(data_input: List[str]) -> int:
    """
    Determines the opcode mapping and executes the program.

    Args:
        data_input (List[str]): Raw input lines.

    Returns:
        int: The value in register 0 after executing the program.
    """
    samples, program = parse_input(data_input)

    # Initialize candidate opcode mappings (each opcode could be any of the 16 functions)
    opcode_candidates: Dict[int, set[str]] = {
        i: set(ALL_OPS.keys()) for i in range(16)
    }

    # Narrow down candidates using the samples
    for before, instr, after in samples:
        opcode = instr[0]
        for name in list(opcode_candidates[opcode]):
            regs = deepcopy(before)
            ALL_OPS[name](regs, *instr[1:])
            if regs != after:
                opcode_candidates[opcode].discard(name)

    # Resolve opcode-function mapping by elimination
    final_opcodes: Dict[int, str] = {}
    while len(final_opcodes) < 16:
        for code, options in opcode_candidates.items():
            options -= set(final_opcodes.values())  # Remove already assigned operations
            if len(options) == 1:
                final_opcodes[code] = options.pop()

    # Execute the actual test program using the resolved opcode mapping
    regs = [0, 0, 0, 0]
    for instr in program:
        opcode = instr[0]
        func = ALL_OPS[final_opcodes[opcode]]
        func(regs, *instr[1:])

    return regs[0]


if __name__ == "__main__":
    input_data = get_input("inputs/16_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
