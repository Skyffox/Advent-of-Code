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


def load_aunts(file_path: str) -> List[Dict[str, int]]:
    """
    Reads the input file, parses each Aunt Sue's attributes into dictionaries.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        List[Dict[str, int]]: List of dictionaries, each representing
            an Aunt Sue's known attributes.
    """
    pattern = re.compile(r"Sue \d+: (.+)")
    aunts = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
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
def part_one(file_path: str) -> int:
    """
    Identifies the Aunt Sue whose attributes exactly match the known gift giver's attributes.

    The known gift attributes are compared exactly against each Sue's attributes.
    Any attribute not specified in a Sue's description is ignored.

    Args:
        file_path (str): Path to the input file describing Aunt Sues.

    Returns:
        int: The number of the Aunt Sue matching the gift attributes exactly.
    """
    aunts = load_aunts(file_path)

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
def part_two(file_path: str) -> int:
    """
    Identifies the Aunt Sue who matches the gift giver's attributes with
    modified comparison rules:

      - For "cats" and "trees", the Sue's value must be greater than the gift's.
      - For "pomeranians" and "goldfish", the Sue's value must be less than the gift's.
      - For all other attributes, the Sue's value must be exactly equal.

    Any attribute not present in a Sue's description is ignored.

    Args:
        file_path (str): Path to the input file describing Aunt Sues.

    Returns:
        int: The number of the Aunt Sue matching the gift attributes with modified rules.
    """
    aunts = load_aunts(file_path)

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
    print(f"Part 1: {part_one('inputs/16_input.txt')}")
    print(f"Part 2: {part_two('inputs/16_input.txt')}")
