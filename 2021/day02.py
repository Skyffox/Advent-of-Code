# pylint: disable=line-too-long
"""
Part 1: Find out what our position is after following the commands
Answer: 2073315

Part 2: Now there is another factor that influences our course
Answer: 1840311528
"""

from utils import profiler


def get_input(file_path: str) -> tuple[list, list]:
    """Get the input data"""
    lst = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            move = line.strip().split(" ")
            units = int(move[1])

            lst.append([move, units])

    return lst


@profiler
def part_1(lst: list) -> int:
    """Follow commands to change the position of the submarine"""
    x, y = 0, 0
    for (move, units) in lst:
        if move[0] == "forward":
            x += units
        elif move[0] == "down":
            y += units
        elif move[0] == "up":
            y -= units

    # Multiply the horizontal position by depth
    return x * y


@profiler
def part_2(lst: list) -> int:
    """There is a new element (the aim) that changes based on the instructions"""
    position, depth, aim = 0, 0, 0
    for (move, units) in lst:
        if move[0] == "forward":
            position += units
            depth += aim * units
        elif move[0] == "down":
            aim += units
        elif move[0] == "up":
            aim -= units

    # Multiply the horizontal position by depth
    return position * depth


if __name__ == "__main__":
    input_data = get_input("inputs/2_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
