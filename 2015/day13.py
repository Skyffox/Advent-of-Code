# pylint: disable=line-too-long
"""
Day 13: Knights of the Dinner Table

Part 1: What is the total change in happiness for the optimal seating arrangement of the actual guest list?
Answer: 664

Part 2: What is the total change in happiness for the optimal seating arrangement that actually includes yourself?
Answer: 640
"""

from typing import List, Dict
import re
import itertools
from utils import profiler


def get_input(file_path: str) -> Dict[str, Dict[str, int]]:
    """
    Reads the input file and parses happiness preferences into a nested dictionary.

    Each line describes the change in happiness between two people when seated together,
    e.g., "Alice would gain 54 happiness units by sitting next to Bob."

    Returns a structure like:
    {
        "Alice": {"Bob": 54, "Carol": -79, ...},
        "Bob": {"Alice": 83, "David": -7, ...},
        ...
    }

    Args:
        file_path (str): Path to the input text file.

    Returns:
        Dict[str, Dict[str, int]]: Mapping person -> neighbor -> happiness change.
    """
    preferences = {}
    pattern = re.compile(r"(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+).")
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            match = pattern.match(line.strip())
            if match:
                person, gain_lose, amount, neighbor = match.groups()
                value = int(amount) if gain_lose == "gain" else -int(amount)
                preferences.setdefault(person, {})[neighbor] = value
    return preferences


def calculate_happiness(arrangement: List[str], preferences: Dict[str, Dict[str, int]]) -> int:
    """
    Calculates the total happiness for a circular seating arrangement.

    Each person contributes happiness based on both neighbors.

    Args:
        arrangement (List[str]): Ordered list of seated people.
        preferences (Dict[str, Dict[str, int]]): Mapping of happiness values.

    Returns:
        int: Total happiness for the seating.
    """
    total = 0
    n = len(arrangement)
    for i in range(n):
        left = arrangement[i]
        right = arrangement[(i + 1) % n]
        total += preferences[left][right] + preferences[right][left]
    return total


@profiler
def part_one(preferences: Dict[str, Dict[str, int]]) -> int:
    """
    Finds the optimal circular seating arrangement (excluding yourself)
    that maximizes the total happiness change, accounting for mutual effects
    between adjacent guests. Uses symmetry optimization by fixing one person
    and permuting the rest.

    Args:
        preferences (Dict[str, Dict[str, int]]): Happiness values for each neighbor pair.

    Returns:
        int: Maximum total happiness for any valid arrangement.
    """
    people = list(preferences.keys())
    first = people[0]
    others = people[1:]

    return max(
        calculate_happiness([first] + list(p), preferences)
        for p in itertools.permutations(others)
    )


@profiler
def part_two(preferences: Dict[str, Dict[str, int]]) -> int:
    """
    Adds yourself ("You") to the guest list with zero happiness change for all interactions.
    Then computes the maximum happiness with the updated list using the same strategy
    as part one.

    Args:
        preferences (Dict[str, Dict[str, int]]): Happiness values for each neighbor pair.

    Returns:
        int: Maximum total happiness including yourself at the table.
    """
    you = "You"
    people = list(preferences.keys())

    preferences[you] = {}
    for person in people:
        preferences[person][you] = 0
        preferences[you][person] = 0
    people.append(you)

    first = people[0]
    others = people[1:]

    return max(
        calculate_happiness([first] + list(p), preferences)
        for p in itertools.permutations(others)
    )


if __name__ == "__main__":
    input_data = get_input("inputs/13_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
