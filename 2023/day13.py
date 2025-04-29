# pylint: disable=line-too-long
"""
Part 1: Find the line of reflection in each of the patterns in your notes. What number do you get after summarizing all of your notes?
Answer: 

Part 2: 
Answer: 
"""

from utils import profiler


def get_input(file_path: str) -> list:
    """Get the input data"""
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

    return file


@profiler
def part_one(data_input):
    """Comment"""


@profiler
def part_two(data_input):
    """Comment"""


if __name__ == "__main__":
    # Get input data
    input_data = get_input("inputs/13_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
