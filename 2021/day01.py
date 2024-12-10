# pylint: disable=line-too-long
"""
Part 1: See how many times there is an increase or decrease in the data
Answer: 1624

Part 2: Instead compare it over a window of 3 items, in this case we only compare the first and the last of that window
Answer: 1653
"""

from utils import profiler


def get_input(file_path: str) -> tuple[list, list]:
    """Get the input data"""
    lst = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            lst.append(int(line.strip()))

    return lst


@profiler
def part_1(lst: list) -> int:
    """a"""
    n = 0
    for x in range(len(lst) - 1):
        if lst[x+1] > lst[x]:
            n += 1
    return n


@profiler
def part_2(lst: list) -> int:
    """a"""
    n = 0
    for x in range(len(lst) - 3):
        if lst[x+3] > lst[x]:
            n += 1
    return n


if __name__ == "__main__":
    input_data = get_input("inputs/1_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
