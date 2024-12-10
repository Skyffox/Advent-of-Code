# pylint: disable=line-too-long
"""
Part 1: Find the floor that Santa ends up on
Answer: 74

Part 2: Find the instruction when Santa first enters the basement
Answer: 1795
"""

from utils import profiler


def get_input(file_path: str) -> list:
    """Get the input data"""
    with open(file_path, "r", encoding="utf-8") as file:
        return "".join(file.readlines())


@profiler
def part_1(lst: list) -> int:
    """Count how many times we go up/down a floor"""
    return lst.count("(") - lst.count(")")


@profiler
def part_2(lst: list) -> int:
    """Find out at what instruction we end up in the basement"""
    floor = 0
    for idx, c in enumerate(lst):
        if c == "(":
            floor += 1
        else:
            floor -= 1

        if floor == -1:
            return idx + 1

    return floor


if __name__ == "__main__":
    INPUT_DATA = get_input("inputs/1_input.txt")

    print(f"Part 1: {part_1(INPUT_DATA)}")
    print(f"Part 2: {part_2(INPUT_DATA)}")
