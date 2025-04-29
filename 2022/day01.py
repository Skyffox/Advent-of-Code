# pylint: disable=line-too-long
"""
Part 1: Find the Elf carrying the most Calories.
Answer: 72240

Part 2: Find the top three Elves carrying the most Calories.
Answer: 210957
"""

from utils import profiler


def get_input(file_path: str) -> list:
    """Get the input data"""
    lst = []
    total = 0
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line == "":
                lst.append(total)
                total = 0
                continue
            total += int(line)

    return lst


@profiler
def part_1(sum_lst: list) -> int:
    """Get the elf with the most calories"""
    return sorted(sum_lst, reverse=True)[0]


@profiler
def part_2(sum_lst: list) -> int:
    """Get the top 3 elves with the most calories"""
    return sum(sorted(sum_lst, reverse=True)[0:3])


if __name__ == "__main__":
    input_data = get_input("inputs/1_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
