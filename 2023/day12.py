# pylint: disable=line-too-long
"""
Day 12: Hot Springs

Part 1: For each row, count all of the different arrangements of operational and broken springs that meet the given criteria. What is the sum of those counts?
Answer: 7407

Part 2: For each row, repeat the pattern 5 times (with separators), and compute the new valid arrangements.
Answer: 30568243604962
"""

from functools import cache
from typing import List, Tuple
from utils import profiler


class Spring:
    """
    A class to represent the state of a Spring system, such as in the context
    of a puzzle or simulation where the spring system can be operational, 
    damaged, or in an unknown state.
    """
    OPERATIONAL = '.'
    DAMAGED = '#'
    UNKNOWN = '?'
    

def get_input(file_path: str) -> List[Tuple[str, List[int]]]:
    """
    Reads the input file and parses each line into a spring pattern and its associated group sizes.

    Args:
        file_path (str): Path to the input file.

    Returns:
        List[Tuple[str, List[int]]]: List of (spring pattern, group sizes).
    """
    output = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            pattern, groups = line.strip().split(" ")
            group_sizes = list(map(int, groups.split(",")))
            output.append((pattern, group_sizes))
    return output


@cache
def count_valid_arrangements(springs: str, notes: Tuple[int, ...], count: int = 0) -> int:
    """
    Recursively counts all valid spring arrangements that match the required damaged groupings.

    Args:
        springs (str): Remaining spring pattern to evaluate.
        notes (Tuple[int, ...]): Tuple of required damaged spring group sizes.
        count (int): Current length of the ongoing damaged group.

    Returns:
        int: Number of valid arrangements matching the criteria.
    """
    if not springs:
        if count > 0:
            return int(len(notes) == 1 and count == notes[0])
        return int(len(notes) == 0)

    if count > 0 and (not notes or count > notes[0]):
        return 0

    first, rest = springs[0], springs[1:]

    match first:
        case Spring.OPERATIONAL:
            if count > 0:
                if not notes or count != notes[0]:
                    return 0
                notes = notes[1:]
            return count_valid_arrangements(rest, notes, 0)

        case Spring.DAMAGED:
            return count_valid_arrangements(rest, notes, count + 1)

        case Spring.UNKNOWN:
            result = 0
            # Try as DAMAGED
            result += count_valid_arrangements(Spring.DAMAGED + rest, notes, count)
            # Try as OPERATIONAL
            result += count_valid_arrangements(Spring.OPERATIONAL + rest, notes, count)
            return result

        case _:
            raise ValueError(f"Invalid spring character: {first}")


def transform_input(springs: str, notes: List[int]) -> Tuple[str, List[int]]:
    """
    Expands the input pattern and notes by repeating them 5 times, with '?' separators.

    Args:
        springs (str): Original spring pattern.
        notes (List[int]): Original group sizes.

    Returns:
        Tuple[str, List[int]]: Expanded spring pattern and note list.
    """
    return '?'.join([springs] * 5), notes * 5


@profiler
def part_one(data: List[Tuple[str, List[int]]]) -> int:
    """
    Solves Part 1 by counting valid arrangements for each pattern without transformation.

    Args:
        data (List[Tuple[str, List[int]]]): Parsed input data.

    Returns:
        int: Total valid arrangements.
    """
    total = 0
    for springs, notes in data:
        total += count_valid_arrangements(springs, tuple(notes))
    return total


@profiler
def part_two(data: List[Tuple[str, List[int]]]) -> int:
    """
    Solves Part 2 by transforming the input and counting valid arrangements.

    Args:
        data (List[Tuple[str, List[int]]]): Parsed input data.

    Returns:
        int: Total valid arrangements after transformation.
    """
    total = 0
    for springs, notes in data:
        expanded_springs, expanded_notes = transform_input(springs, notes)
        total += count_valid_arrangements(expanded_springs, tuple(expanded_notes))
    return total


if __name__ == "__main__":
    input_data = get_input("inputs/12_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
