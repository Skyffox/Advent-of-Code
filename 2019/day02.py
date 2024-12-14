# pylint: disable=line-too-long
"""
Part 1: 
Answer: 3790645

Part 2: 
Answer:
"""

from utils import profiler
from copy import deepcopy


def operation(op, x, y):
    """a"""
    if op == 1:
        return x + y
    if op == 2:
        return x * y


def get_input(file_path: str) -> tuple[list, list]:
    """Get the input data"""
    instructions = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            instructions = list(map(int, line.strip().split(",")))

    return instructions


@profiler
def part_1(instructions: list) -> int:
    """a"""
    instructions[1] = 12
    instructions[2] = 2

    for idx in range(len(instructions) // 4):
        operator = instructions[idx*4]
        x = instructions[idx*4+1]
        y = instructions[idx*4+2]
        output_idx = instructions[idx*4+3]

        if operator == 99:
            return instructions[0]

        instructions[output_idx] = operation(operator, instructions[x], instructions[y])


@profiler
def part_2(instructions: list) -> int:
    """a"""
    # instruction_ptr = 0
    answer = 19690720
       
    for i in range(1, 99):
        for j in range(1, 99):
            instructions[1] = i
            instructions[2] = j
            instructions_cpy = deepcopy(instructions)
            for idx in range(len(instructions_cpy) // 4):
                operator = instructions_cpy[idx*4]
                x = instructions_cpy[idx*4+1]
                y = instructions_cpy[idx*4+2]
                output_idx = instructions_cpy[idx*4+3]

                if operator == 99:
                    if instructions_cpy[0] == answer:
                        return 100 * i + j
                    else:
                        break
                # print(operator, instructions_cpy[x], instructions_cpy[y])
                instructions_cpy[output_idx] = operation(operator, instructions_cpy[x], instructions_cpy[y])



if __name__ == "__main__":
    input_data = get_input("inputs/2_input.txt")

    input_data_cpy = deepcopy(input_data)

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data_cpy)}")
