# pylint: disable=line-too-long
"""
Day 12: JSAbacusFramework.io

Part 1: What is the sum of all numbers in the document?
Answer: 111754

Part 2: Ignore any object (and all of its children) which has any property with the value "red". 
Answer: 65402
"""

from typing import List, Any
import json
from utils import profiler


def get_input(file_path: str) -> List[str]:
    """
    Reads the input file and returns a list of stripped lines.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        list[str]: A list of lines with leading/trailing whitespace removed.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file]


@profiler
def part_one(data_input: List[str]) -> int:
    """
    Sums all numbers in the input JSON, regardless of structure.

    Args:
        data_input (List[str]): A list of input lines.

    Returns:
        int: Sum of all numbers.
    """
    text = data_input[0].replace('[', ' ').replace(']', ' ').replace('{', ' ').replace('}', ' ').replace(',', ' ').replace(':', ' ').split()
    return sum([int(n) for n in text if n.lstrip('-').isdigit()])


def sum_json_excluding_red(data: Any) -> int:
    """
    Recursively sums all numbers in the JSON data, excluding any objects
    (dicts) with a value "red".

    Args:
        data (Any): Parsed JSON data.

    Returns:
        int: The conditional sum of numbers.
    """
    if isinstance(data, int):
        return data
    elif isinstance(data, list):
        return sum(sum_json_excluding_red(item) for item in data)
    elif isinstance(data, dict):
        if "red" in data.values():
            return 0
        return sum(sum_json_excluding_red(val) for val in data.values())
    else:
        return 0


@profiler
def part_two(data_input: List[str]) -> int:
    """
    Sums all numbers in the input JSON, excluding any object with "red".

    Args:
        data_input (List[str]): A list of input lines.

    Returns:
        int: Conditional sum of numbers.
    """
    json_data = json.loads(data_input[0])
    return sum_json_excluding_red(json_data)


if __name__ == "__main__":
    input_data = get_input("inputs/12_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
