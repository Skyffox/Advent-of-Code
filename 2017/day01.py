# pylint: disable=line-too-long
"""
Part 1: Find the sum of all digits that match the next digit in the list and the list must be circular
Answer: 1253

Part 2: Do the same but now check not the next digit but the digit halfway further up the list
Answer: 1278
"""

from utils import profiler


def get_input(file_path: str) -> list:
    """Get the input data"""
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            return list(map(int, line.strip()))


@profiler
def part_1(lst: list) -> int:
    """Check an item in the list against the next one, the second part is to satisfy the circular requirement"""
    return sum([i for i, j in zip(lst, lst[1:]) if i == j]) + int(lst[0] == lst[-1])


@profiler
def part_2(lst: list) -> int:
    """Do the same as part_1() but check with the middle of the list"""
    return sum([2 * i for i, j in zip(lst, lst[len(lst)//2:]) if i == j])


if __name__ == "__main__":
    input_data = get_input("inputs/1_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
