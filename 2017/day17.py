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
    Finds the value after 0 after 50 million insertions in the spinlock.

    The spinlock algorithm inserts values into a circular buffer by moving forward
    `step_size` steps and inserting the next value. Naively simulating all insertions
    requires storing and updating a huge list, which is prohibitively expensive for
    50 million insertions.

    This optimized approach avoids storing the entire buffer by:
    - Tracking only the current position (`pos`) of the insertion cursor.
    - Keeping track of the buffer length (`length`), which grows by one each insertion.
    - Recording the value inserted immediately after 0, since the problem asks only
      for the value following 0 in the final buffer.
    
    How it works:
    - The position `pos` is updated each iteration using modular arithmetic to simulate
      movement around the circular buffer.
    - When `pos == 1`, it means the new value is inserted immediately after 0.
      The algorithm then updates `value_after_zero` to this newly inserted value.
    - No actual list is maintained, so memory usage is constant.
    - Each iteration runs in O(1) time, allowing 50 million iterations to complete efficiently.

    Args:
        step_size (int): Number of steps to move forward before inserting.

    Returns:
        int: The value immediately following 0 after 50 million insertions.
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
