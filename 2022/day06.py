# pylint: disable=line-too-long
"""
Day 6: Tuning Trouble

Part 1: How many characters need to be processed before the first start-of-packet marker is detected?
Answer: 1850

Part 2: How many characters need to be processed before the first start-of-message marker is detected?
Answer: 2823
"""

from utils import profiler


def get_input(file_path: str) -> list[str]:
    """
    Read a single line from the input file and return it as a list of characters.

    Args:
        file_path (str): Path to the input file.

    Returns:
        list[str]: List of characters from the input line.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return list(file.readline().strip())


@profiler
def find_marker_position(data: list[str], window_size: int) -> int:
    """
    Find the position where a marker of `window_size` distinct characters first appears.

    Args:
        data (list[str]): List of characters from the input.
        window_size (int): Number of distinct characters to look for in a window.

    Returns:
        int: Index after the marker (number of characters processed).
    """
    for i in range(len(data) - window_size + 1):
        window = data[i:i + window_size]
        if len(set(window)) == window_size:
            return i + window_size


if __name__ == "__main__":
    input_data = get_input("inputs/6_input.txt")

    print(f"Part 1: {find_marker_position(input_data, 4)}")
    print(f"Part 2: {find_marker_position(input_data, 14)}")
