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
    with open(file_path, "r", encoding="utf-8") as file:
        return [int(line.strip()) for line in file]


@profiler
def part_1(lst: list) -> int:
    """Compare each subsequent number in a list and detect each time an increase happens"""
    return sum([1 for i in range(len(lst) - 1) if lst[i + 1] > lst[i]])


@profiler
def part_2(lst: list) -> int:
    """Compare over steps of 3 and compare the first and last of each step to determine an increase or decrease"""
    return sum([1 for i in range(len(lst) - 3) if lst[i + 3] > lst[i]])


if __name__ == "__main__":
    input_data = get_input("inputs/1_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
