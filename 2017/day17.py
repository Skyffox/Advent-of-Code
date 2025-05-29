# pylint: disable=line-too-long
"""
Day 17: Spinlock

Part 1: What is the value after 2017 in your completed circular buffer?
Answer: 808

Part 2: What is the value after 0 the moment 50000000 is inserted?
Answer: 47465686
"""

from utils import profiler


def get_input(file_path: str) -> int:
    """
    Reads the input file and returns the step size.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        int: Step size as integer.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return int(file.readline().strip())


@profiler
def part_one(step_size: int) -> int:
    """
    Simulates the spinlock for 2017 insertions and returns the value after 2017.

    Args:
        step_size (int): Number of steps to move forward before inserting.

    Returns:
        int: Value immediately after 2017 in the buffer.
    """
    buffer = [0]
    pos = 0
    for i in range(1, 2018):
        pos = (pos + step_size) % len(buffer) + 1
        buffer.insert(pos, i)
    return buffer[pos + 1]


@profiler
def part_two(step_size: int) -> int:
    """
    Finds the value after 0 after 50 million insertions (optimized).

    Args:
        step_size (int): Number of steps to move forward before inserting.

    Returns:
        int: Value immediately after 0.
    """
    pos = 0
    value_after_zero = None
    length = 1

    for i in range(1, 50_000_001):
        pos = (pos + step_size) % length + 1
        if pos == 1:
            value_after_zero = i
        length += 1

    return value_after_zero


if __name__ == "__main__":
    step = get_input("inputs/17_input.txt")

    print(f"Part 1: {part_one(step)}")
    print(f"Part 2: {part_two(step)}")
