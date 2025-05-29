# pylint: disable=line-too-long
"""
Day 16: Aunt Sue

Part 1: What is the number of the Sue that got you the gift?
Answer: 373

Part 2: What is the number of the real Aunt Sue?
Answer: 260
"""

from typing import List, Dict
import re
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


def parse_aunts(data: List[str]) -> List[Dict[str, int]]:
    """
    Parses each Aunt Sue's description into a dictionary.

    Args:
        data (List[str]): List of lines describing each Aunt Sue.

    Returns:
        List[Dict[str, int]]: List of dictionaries of Aunt Sue's attributes.
    """
    aunts = []
    pattern = re.compile(r"Sue \d+: (.+)")
    for line in data:
        match = pattern.match(line)
        if not match:
            continue
        attributes_part = match.group(1)
        attributes = {}
        for attr in attributes_part.split(", "):
            key, value = attr.split(": ")
            attributes[key] = int(value)
        aunts.append(attributes)
    return aunts


@profiler
def part_one(data_input: List[str]) -> int:
    """
    Finds the Aunt Sue that matches the gift giver's attributes exactly.

    Args:
        data_input (List[str]): Input lines describing Aunt Sues.

    Returns:
        int: The number of the matching Aunt Sue.
    """
    aunts = parse_aunts(data_input)

    # Gift giver's known attributes
    gift = {
        "children": 3,
        "cats": 7,
        "samoyeds": 2,
        "pomeranians": 3,
        "akitas": 0,
        "vizslas": 0,
        "goldfish": 5,
        "trees": 3,
        "cars": 2,
        "perfumes": 1,
    }

    for i, aunt in enumerate(aunts, 1):
        if all(aunt.get(k, v) == v for k, v in gift.items()):
            return i


    return -1


@profiler
def part_two(data_input: List[str]) -> int:
    """
    Finds the Aunt Sue that matches the gift giver's attributes with
    modified comparison rules.

    Args:
        data_input (List[str]): Input lines describing Aunt Sues.

    Returns:
        int: The number of the matching Aunt Sue.
    """
    aunts = parse_aunts(data_input)

    gift = {
        "children": 3,
        "cats": 7,
        "samoyeds": 2,
        "pomeranians": 3,
        "akitas": 0,
        "vizslas": 0,
        "goldfish": 5,
        "trees": 3,
        "cars": 2,
        "perfumes": 1,
    }

    for i, aunt in enumerate(aunts, 1):
        match = True
        for key, val in aunt.items():
            if key in ["cats", "trees"]:
                if val <= gift[key]:
                    match = False
                    break
            elif key in ["pomeranians", "goldfish"]:
                if val >= gift[key]:
                    match = False
                    break
            else:
                if val != gift[key]:
                    match = False
                    break
        if match:
            return i

    return -1


if __name__ == "__main__":
    input_data = get_input("inputs/16_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
