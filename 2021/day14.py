# pylint: disable=line-too-long
"""
Day 14: Extended Polymerization

Part 1: Apply 10 steps of pair insertion to the polymer template and find the most and least common elements in the result.
        What do you get if you take the quantity of the most common element and subtract the quantity of the least common element?
Answer: 3247

Part 2: Apply 40 steps of pair insertion to the polymer template and find the most and least common elements in the result.
        What do you get if you take the quantity of the most common element and subtract the quantity of the least common element?
Answer: 4110568157153
"""

from typing import Tuple, Dict
from collections import Counter
from utils import profiler


def get_input(file_path: str) -> Tuple[str, Dict[str, str]]:
    """
    Reads the input file and returns the initial polymer template and pair insertion rules.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        Tuple[str, Dict[str, str]]: Polymer template and insertion rules.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file.readlines() if line.strip()]

    template = lines[0]
    rules = {}
    for line in lines[1:]:
        pair, insert = line.split(" -> ")
        rules[pair] = insert

    return template, rules


def step(template_pairs: Dict[str, int], rules: Dict[str, str]) -> Dict[str, int]:
    """
    Performs one step of polymerization on pairs.

    Args:
        template_pairs (Dict[str, int]): Current pairs with their counts.
        rules (Dict[str, str]): Pair insertion rules.

    Returns:
        Dict[str, int]: Updated pairs after insertion.
    """
    new_pairs = Counter()
    for pair, count in template_pairs.items():
        if pair in rules:
            insert = rules[pair]
            new_pairs[pair[0] + insert] += count
            new_pairs[insert + pair[1]] += count
        else:
            new_pairs[pair] += count
    return new_pairs


def count_elements(template_pairs: Dict[str, int], first_char: str, last_char: str) -> Dict[str, int]:
    """
    Counts elements from pair counts.

    Args:
        template_pairs (Dict[str, int]): Pairs with counts.
        first_char (str): First character of original template.
        last_char (str): Last character of original template.

    Returns:
        Dict[str, int]: Element counts.
    """
    counts = Counter()
    for pair, count in template_pairs.items():
        counts[pair[0]] += count
        counts[pair[1]] += count
    # Every element is counted twice except first and last
    counts[first_char] += 1
    counts[last_char] += 1
    for element in counts:
        counts[element] //= 2
    return counts


@profiler
def compute(data_input: Tuple[str, Dict[str, str]], steps: int) -> int:
    """
    Runs polymerization steps and returns the difference between most and least common elements.

    Args:
        data_input (Tuple[str, Dict[str, str]]): Polymer template and insertion rules.

    Returns:
        int: Difference of counts.
    """
    template, rules = data_input
    template_pairs = Counter(template[i:i + 2] for i in range(len(template) - 1))

    for _ in range(steps):
        template_pairs = step(template_pairs, rules)

    counts = count_elements(template_pairs, template[0], template[-1])
    return max(counts.values()) - min(counts.values())


if __name__ == "__main__":
    input_data = get_input("inputs/14_input.txt")

    print(f"Part 1: {compute(input_data, 10)}")
    print(f"Part 2: {compute(input_data, 40)}")
