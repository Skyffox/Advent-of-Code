# pylint: disable=line-too-long
"""
Day 17: Chronospatial Computer

Part 1: Using the information provided by the debugger, initialize the registers to the given values. 
        Then run the program. Once it halts, what do you get if you use commas to join the values it output into a single string?
Answer: 7,0,3,1,2,6,3,7,1

Part 2: What is the lowest positive initial value for register A that causes the program to output a copy of itself?
Answer: 109020013201563
"""

from typing import List, Tuple
from utils import profiler


def get_input(file_path: str) -> Tuple[int, List[int]]:
    """
    Parses the input file and extracts the initial value for register A and the program instructions.

    Returns:
        Tuple[int, List[int]]: Initial value for register A and the program (list of integers).
    """
    with open(file_path, "r", encoding="utf-8") as file:
        data = file.readlines()
        a = int(''.join([char for char in data[0] if char.isdigit()]))
        program = list(map(int, [char for char in data[4] if char.isdigit()]))
    return a, program


def part_1(program: List[int], register_a: int, register_b: int, register_c: int) -> List[int]:
    """
    Executes a custom virtual machine program, manipulating three registers and producing output.

    Args:
        program (List[int]): The list of opcodes and operands.
        register_a (int): Initial value for register A.
        register_b (int): Initial value for register B.
        register_c (int): Initial value for register C.

    Returns:
        List[int]: Output values produced by the program.
    """
    ptr = 0
    out: List[int] = []

    def combo(operand: int) -> int:
        return {4: register_a, 5: register_b, 6: register_c}.get(operand, operand)

    while ptr < len(program):
        opcode, operand = program[ptr:ptr + 2]

        match opcode:
            case 0:
                register_a >>= combo(operand)
            case 1:
                register_b ^= operand
            case 2:
                register_b = combo(operand) % 8
            case 3:
                if register_a != 0:
                    ptr = operand - 2
            case 4:
                register_b ^= register_c
            case 5:
                out.append(combo(operand) % 8)
            case 6:
                register_b = register_a >> combo(operand)
            case 7:
                register_c = register_a >> combo(operand)

        ptr += 2

    return out


@profiler
def part_2(program: List[int]) -> int:
    """
    Determines the smallest initial value of register A that causes the program to output itself.

    Args:
        program (List[int]): The program instructions (used also as the desired output).

    Returns:
        int: The smallest valid value for register A that produces the same output as the program.
    """
    register_a = 0
    for i in reversed(range(len(program))):
        register_a *= 8
        while part_1(program, register_a, 0, 0) != program[i:]:
            register_a += 1
    return register_a


if __name__ == "__main__":
    A_input, program_input = get_input("inputs/17_input.txt")

    print(f"Part 1: {part_1(program_input, A_input, 0, 0)}")
    print(f"Part 2: {part_2(program_input)}")
