# pylint: disable=line-too-long
"""
Part 1: Follow the instructions to see how many houses Santa can visit
Answer: 2565

Part 2: Take turns between Santa and Robo-Santa and see how many houses they can visit
Answer: 2639
"""

from utils import profiler


def move(x: int, y: int, instruction: str, visited: dict) -> tuple[dict, int, int]:
    """Move based on the instruction, then update the dictionary where we have visited"""
    if instruction == ">":
        x += 1
    elif instruction == "<":
        x -= 1
    elif instruction == "^":
        y += 1
    else:
        y -= 1

    # Update the dictionary if we already visited
    if visited.get((x, y)):
        visited[(x, y)] += 1
    else:
        visited.update({(x, y) : 1})

    return visited, x, y


def get_input(file_path: str) -> list:
    """Get the input data"""
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            instructions = list(line.strip())

    return instructions


@profiler
def part_1(instructions: list) -> int:
    """Follow instructions and count the amount of tiles we visit"""
    x, y = 0, 0
    visited = {(0, 0) : 1}
    for instruction in instructions:
        visited, x, y = move(x, y, instruction, visited)

    return len(visited)


@profiler
def part_2(instructions: list) -> int:
    """Santa and robo-Santa share turns"""
    x, y, x_robo, y_robo = 0, 0, 0, 0
    visited = {(0, 0) : 2}
    for turn, instruction in enumerate(instructions):
        # Santas turn
        if turn % 2 == 0:
            visited, x, y = move(x, y, instruction, visited)
        # Robo-santas turn
        else:
            visited, x_robo, y_robo = move(x_robo, y_robo, instruction, visited)

    return len(visited)


if __name__ == "__main__":
    instr = get_input("inputs/3_input.txt")

    print(f"Part 1: {part_1(instr)}")
    print(f"Part 2: {part_2(instr)}")
