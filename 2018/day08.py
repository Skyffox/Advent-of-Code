# pylint: disable=line-too-long
"""
Day 8: Memory Maneuver

Part 1: What is the sum of all metadata entries?
Answer: 36307

Part 2: What is the value of the root node?
Answer: 25154
"""

from typing import List
from utils import profiler


def get_input(file_path: str) -> List[int]:
    """
    Reads the input file and returns a list of integers.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        list[int]: A list of integers.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return list(map(int, file.read().split()))


def parse_node(data: List[int], is_part2: bool) -> tuple[int, List[int]]:
    """
    Parses a node from the data list.

    Args:
        data (List[int]): The data list.

    Returns:
        tuple[int, List[int]]: A tuple containing the node value and the remaining data list.
    """
    num_children, num_metadata = data[:2]
    data = data[2:]
    children = []
    for _ in range(num_children):
        child_value, data = parse_node(data, is_part2)
        children.append(child_value)
    metadata = data[:num_metadata]
    data = data[num_metadata:]
    if is_part2:
        if num_children == 0:
            return sum(metadata), data
        value = 0
        for m in metadata:
            if 1 <= m <= num_children:
                value += children[m - 1]
        return value, data
    return sum(children) + sum(metadata), data


@profiler
def part_one(data_input: List[int]) -> int:
    """
    Solves part one of the problem using the provided input data.

    Args:
        data_input (List[int]): A list of integers representing the data.

    Returns:
        int: The sum of all metadata entries.
    """
    value, _ = parse_node(data_input, False)
    return value


@profiler
def part_two(data_input: List[int]) -> int:
    """
    Solves part two of the problem using the provided input data.

    Args:
        data_input (List[int]): A list of integers representing the data.

    Returns:
        int: The value of the root node.
    """
    value, _ = parse_node(data_input, True)
    return value


if __name__ == "__main__":
    input_data = get_input("inputs/8_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
