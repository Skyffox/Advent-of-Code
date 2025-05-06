# pylint: disable=line-too-long
"""
Day 2: Inventory Management System

Part 1: Calculate the checksum of box IDs based on the number of letters that appear exactly two or three times.  
Answer: 7192

Part 2: Identify the two correct box IDs that differ by exactly one character at the same position.  
Answer: mbruvapghxlzycbhmfqjonsie
"""

from typing import List
from collections import Counter
from utils import profiler


def get_input(file_path: str) -> List[List[str]]:
    """
    Reads the box IDs from the input file.

    Args:
        file_path (str): Path to the input file.

    Returns:
        List[List[str]]: A list of box IDs, where each ID is a list of characters.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [list(line.strip()) for line in file]


@profiler
def part_1(box_ids: List[List[str]]) -> int:
    """
    Calculates a checksum based on how many IDs contain letters appearing exactly twice or three times.

    Args:
        box_ids (List[List[str]]): List of box IDs as character lists.

    Returns:
        int: The checksum (doubles * triples).
    """
    doubles = triples = 0

    for box_id in box_ids:
        counts = Counter(box_id).values()
        if 2 in counts:
            doubles += 1
        if 3 in counts:
            triples += 1

    return doubles * triples


@profiler
def part_2(box_ids: List[List[str]]) -> str:
    """
    Finds the common letters between the two box IDs that differ by exactly one character.

    Args:
        box_ids (List[List[str]]): List of box IDs as character lists.

    Returns:
        str: The common characters between the two correct box IDs.
    """
    for i, id1 in enumerate(box_ids):
        for id2 in box_ids[i + 1:]:
            differences = [a != b for a, b in zip(id1, id2)]
            if sum(differences) == 1:
                # Get characters that matched
                return ''.join(a for a, b in zip(id1, id2) if a == b)

    return "" # Fallback if no match is found


if __name__ == "__main__":
    input_data = get_input("inputs/2_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
