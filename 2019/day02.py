# pylint: disable=line-too-long
"""
Part 1: What value is left at position 0 after the program halts?
Answer: 3790645

Part 2: Find the input noun and verb that cause the program to produce the output 19690720 through the formula: 100 * noun + verb
Answer: 6577
"""

from copy import deepcopy
from utils import profiler


def operation(op, x, y):
    """Input has different operations for different answers"""
    if op == 1:
        return x + y
    if op == 2:
        return x * y


def get_input(file_path: str) -> tuple[list, list]:
    """Get the input data"""
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            return list(map(int, line.strip().split(",")))


@profiler
def part_1(instructions: list) -> int:
    """The input holds different operations of which we must calculate the answers and put them in specific locations of the input list"""
    instructions[1] = 12
    instructions[2] = 2

    for idx in range(len(instructions) // 4):
        operator = instructions[idx * 4]
        x = instructions[idx * 4 + 1]
        y = instructions[idx * 4 + 2]
        output_idx = instructions[idx * 4 + 3]

        # The program halts
        if operator == 99:
            return instructions[0]

        instructions[output_idx] = operation(operator, instructions[x], instructions[y])


@profiler
def part_2(instructions: list) -> int:
    """Continue on the same path as part 1 but now we must figure out for which inputs the program halts on value 19690720"""
    answer = 19690720

    for i in range(1, 99):
        for j in range(1, 99):
            instructions[1] = i
            instructions[2] = j
            instructions_cpy = deepcopy(instructions)
            for idx in range(len(instructions_cpy) // 4):
                operator = instructions_cpy[idx * 4]
                x = instructions_cpy[idx * 4 + 1]
                y = instructions_cpy[idx * 4 + 2]
                output_idx = instructions_cpy[idx * 4 + 3]

                # The program halts
                if operator == 99:
                    if instructions_cpy[0] == answer:
                        return 100 * i + j
                    else:
                        break

                instructions_cpy[output_idx] = operation(operator, instructions_cpy[x], instructions_cpy[y])


if __name__ == "__main__":
    input_data = get_input("inputs/2_input.txt")

    input_data_cpy = deepcopy(input_data)

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data_cpy)}")
