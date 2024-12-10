# pylint: disable=line-too-long
"""
Part 1: Find two numbers in the input that add together to 2020
Answer: 445536

Part 2: Now do the same but for 3 numbers
Answer: 138688160
"""

from utils import profiler


def get_input(file_path: str) -> list:
    """Get the input data"""
    lst = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            lst.append(int(line.strip()))

    return lst


@profiler
def part_1(lst: list) -> int:
    """Find 2 numbers that add up to 2020"""
    for idx, x in enumerate(lst):
        for y in lst[idx+1:]:
            if x + y == 2020:
                return x * y


@profiler
def part_2(lst: list) -> int:
    """Find 3 numbers that add up to 2020"""
    for idx, x in enumerate(lst):
        for y in enumerate(lst[idx+1:]):
            for z in lst[idx+1:]:
                if x + y + z == 2020:
                    return x * y * z


if __name__ == "__main__":
    input_data = get_input("inputs/1_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
