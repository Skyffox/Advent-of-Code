# pylint: disable=line-too-long
"""
Part 1: Find the item type that appears in both compartments of each rucksack. What is the sum of the priorities of those item types?
Answer: 7845

Part 2: Find the item type that corresponds to the badges of each three-Elf group. What is the sum of the priorities of those item types?
Answer: 2790
"""

from utils import profiler


def get_input(file_path: str) -> list:
    """Get the input data"""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.readlines()


@profiler
def part_1(lines: list) -> int:
    """Split the string in two and find similar items."""
    s = 0
    for i, item in enumerate(lines):
        line = list(item.strip())
        first_compartment = line[:len(line)//2]
        second_compartment = line[len(line)//2:]

        for item in first_compartment:
            if item in second_compartment:
                common = item
                break

        # Account for offset
        if common.isupper():
            s += ord(common) - 38
        else:
            s += ord(common) - 96

    return s


@profiler
def part_2(lines: list) -> int:
    """Find similar items, 3 lines at a time."""
    s = 0
    for i in range(0, len(lines), 3):
        for item in lines[i]:
            if item in lines[i+1] and item in lines[i+2]:
                common = item
                break

        if common.isupper():
            s += ord(common) - 38
        else:
            s += ord(common) - 96
    return s


if __name__ == "__main__":
    input_data = get_input("inputs/3_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
