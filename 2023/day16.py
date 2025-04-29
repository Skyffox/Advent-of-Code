# pylint: disable=line-too-long
"""
Part 1: The light isn't energizing enough tiles to produce lava; to debug the contraption, you need to start by analyzing the current situation. 
        With the beam starting in the top-left heading right, how many tiles end up being energized?
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
    input_data = get_input("inputs/16_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
