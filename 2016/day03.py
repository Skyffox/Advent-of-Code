# pylint: disable=line-too-long
"""
Part 1: Find all valid triangles, where the two smallest sides must be bigger than the largest side
Answer: 917

Part 2: Look at the first column of the input and determine the same thing from there
Answer: 1649
"""

from copy import deepcopy
from utils import profiler


def get_input(file_path: str) -> list:
    """Get the input data"""
    lst = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            lst.append(list(map(int, line.split())))

    return lst


@profiler
def part_1(lst: list) -> int:
    """Sort the list to find the smallest sides"""
    n = 0
    for line in lst:
        line.sort()
        if line[0] + line[1] > line[2]:
            n += 1

    return n


@profiler
def part_2(lst: list) -> int:
    """Take 3 sublists and compare the indices of these sublists to form a triangle"""
    n = 0
    for i in range(len(lst) // 3):
        for j in range(3):
            # Determine the vertical values from the column
            ln = [lst[i * 3][j], lst[i * 3 + 1][j], lst[i * 3 + 2][j]]
            ln.sort()
            if ln[0] + ln[1] > ln[2]:
                n += 1

    return n


if __name__ == "__main__":
    input_data = get_input("inputs/3_input.txt")
    input_data_cpy = deepcopy(input_data)

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data_cpy)}")
