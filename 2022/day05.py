# pylint: disable=line-too-long
"""
Part 1: After the rearrangement procedure completes, what crate ends up on top of each stack?
Answer: DHBJQJCCW

Part 2: After the rearrangement procedure completes, what crate ends up on top of each stack?
Answer: WJVRLSJJT
"""

from copy import deepcopy
from utils import profiler


def get_input(file_path: str) -> list:
    """Get the input data"""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.readlines()


@profiler
def part_1(lines: list, stacks: list) -> str:
    """a"""
    for line in lines:
        line = list(line.strip().split(" "))

        if line[0] == "move":
            move = [int(x) for x in line if x.isdigit()]

            for _ in range(move[0]):
                crate = stacks[move[1] - 1].pop()
                stacks[move[2] - 1].append(crate)

    return "".join([s.pop() for s in stacks])


@profiler
def part_2(lines: list, stacks: list) -> str:
    """A"""
    for line in lines:
        line = list(line.strip().split(" "))

        if line[0] == "move":
            move = [int(x) for x in line if x.isdigit()]
            stacks[move[2] - 1] += stacks[move[1] - 1][-move[0]:]
            for _ in range(move[0]):
                stacks[move[1] - 1].pop()

    return "".join([s.pop() for s in stacks])


if __name__ == "__main__":
    input_data = get_input("inputs/5_input.txt")

    stack = [
        ["F", "C", "P", "G", "Q", "R"],
        ["W", "T", "C", "P"],
        ["B", "H", "P", "M", "C"],
        ["L", "T", "Q", "S", "M", "P", "R"],
        ["P", "H", "J", "Z", "V", "G", "N"],
        ["D", "P", "J"],
        ["L", "G", "P", "Z", "F", "J", "T", "R"],
        ["N", "L", "H", "C", "F", "P", "T", "J"],
        ["G", "V", "Z", "Q", "H", "T", "C", "W"]
    ]

    print(f"Part 1: {part_1(input_data, deepcopy(stack))}")
    print(f"Part 2: {part_2(input_data, stack)}")
