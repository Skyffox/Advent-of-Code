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


def parse_preferences(data: List[str]) -> Dict[str, Dict[str, int]]:
    """
    Parses the happiness preferences into a nested dictionary.

    Args:
        data (List[str]): Lines describing happiness effects.

    Returns:
        Dict[str, Dict[str, int]]: Mapping person -> neighbor -> happiness effect.
    """
    preferences = {}
    pattern = re.compile(r"(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+).")
    for line in data:
        match = pattern.match(line)
        if not match:
            continue
        person, gain_lose, amount, neighbor = match.groups()
        amount = int(amount) if gain_lose == "gain" else -int(amount)
        preferences.setdefault(person, {})[neighbor] = amount
    return preferences


def calculate_happiness(arrangement: List[str], preferences: Dict[str, Dict[str, int]]) -> int:
    """
    Calculates the total happiness for a circular seating arrangement.

    Args:
        arrangement (List[str]): Ordered list of people around the table.
        preferences (Dict[str, Dict[str, int]]): Happiness mapping.

    Returns:
        int: Total happiness for the arrangement.
    """
    total = 0
    n = len(arrangement)
    for i in range(n):
        left = arrangement[i]
        right = arrangement[(i + 1) % n]
        total += preferences[left][right] + preferences[right][left]
    return total


@profiler
def part_one(data_input: List[str]) -> int:
    """
    Finds the optimal seating arrangement maximizing total happiness.

    Args:
        data_input (List[str]): Input lines with preferences.

    Returns:
        int: Maximum total happiness.
    """
    preferences = parse_preferences(data_input)
    people = list(preferences.keys())

    # Fix one person to reduce permutations due to circular symmetry
    first = people[0]
    others = people[1:]

    max_happiness = max(
        calculate_happiness([first] + list(p), preferences)
        for p in itertools.permutations(others)
    )
    return max_happiness


@profiler
def part_two(data_input: List[str]) -> int:
    """
    Finds the optimal seating including yourself (0 happiness with others).

    Args:
        data_input (List[str]): Input lines with preferences.

    Returns:
        int: Maximum total happiness including yourself.
    """
    preferences = parse_preferences(data_input)
    people = list(preferences.keys())
    you = "You"

    # Add yourself with zero happiness effects to everyone
    preferences[you] = {}
    for person in people:
        preferences[person][you] = 0
        preferences[you][person] = 0

    people.append(you)

    # Fix one person to reduce permutations due to circular symmetry
    first = people[0]
    others = people[1:]

    max_happiness = max(
        calculate_happiness([first] + list(p), preferences)
        for p in itertools.permutations(others)
    )
    return max_happiness


if __name__ == "__main__":
    input_data = get_input("inputs/13_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
