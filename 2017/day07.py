# pylint: disable=line-too-long
"""
Day 7: Recursive Circus

Part 1: What is the name of the bottom program?
Answer: dtacyn

Part 2: Given that exactly one program is the wrong weight, what would its weight need to be to balance the entire tower?
Answer: 521
"""

import re
from typing import List, Dict, Tuple
from utils import profiler


def get_input(file_path: str) -> List[str]:
    """
    Reads the input file and returns a list of lines describing programs.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        List[str]: List of program description lines.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file]


def parse_programs(lines: List[str]) -> Tuple[Dict[str, int], Dict[str, List[str]]]:
    """
    Parses program weights and children from input lines.

    Args:
        lines (List[str]): Input lines describing programs.

    Returns:
        Tuple:
            weights (Dict[str, int]): Program name to weight.
            children (Dict[str, List[str]]): Program name to list of child programs.
    """
    weights, children = {}, {}
    pattern = re.compile(r"(\w+)\s+\((\d+)\)(?:\s+->\s+([\w\s,]+))?")
    for line in lines:
        match = pattern.match(line)
        if match:
            name, weight, kids = match.groups()
            weights[name] = int(weight)
            if kids is not None:
                children[name] = [k.strip() for k in kids.split(",")]
            else:
                children[name] = []

    return weights, children


def find_root(children: Dict[str, List[str]]) -> str:
    """
    Finds the root program (the one not listed as child).

    Args:
        children (Dict[str, List[str]]): Program children map.

    Returns:
        str: The root program name.
    """
    all_nodes = set(children.keys())
    child_nodes = {c for kids in children.values() for c in kids}
    root = list(all_nodes - child_nodes)[0]
    return root


def compute_weight(name: str, weights: Dict[str, int], children: Dict[str, List[str]], memo: Dict[str, int]) -> int:
    """
    Recursively computes total weight of a program including children.

    Args:
        name (str): Program name.
        weights (Dict[str, int]): Program weights.
        children (Dict[str, List[str]]): Program children.
        memo (Dict[str, int]): Memoization dict.

    Returns:
        int: Total weight of program.
    """
    if name in memo:
        return memo[name]
    total = weights[name] + sum(compute_weight(c, weights, children, memo) for c in children[name])
    memo[name] = total
    return total


def find_unbalance(name: str, weights: Dict[str, int], children: Dict[str, List[str]]) -> int:
    """
    Finds the corrected weight to balance the tower.

    Args:
        name (str): Root program name.
        weights (Dict[str, int]): Program weights.
        children (Dict[str, List[str]]): Program children.

    Returns:
        int: Corrected weight for unbalanced program.
    """
    memo = {}

    def helper(node: str) -> Tuple[int, int]:
        # returns (total_weight, corrected_weight or 0 if none)
        child_weights = [compute_weight(c, weights, children, memo) for c in children[node]]
        weight_counts = {}
        for w in child_weights:
            weight_counts[w] = weight_counts.get(w, 0) + 1

        if len(weight_counts) <= 1:
            return weights[node] + sum(child_weights), 0

        # Find the unbalanced weight and the balanced weight
        correct_weight = max(weight_counts, key=weight_counts.get)
        wrong_weight = min(weight_counts, key=weight_counts.get)

        # Find which child is unbalanced
        for c, w in zip(children[node], child_weights):
            if w == wrong_weight:
                _, correction = helper(c)
                if correction != 0:
                    return 0, correction
                # Calculate the weight adjustment needed
                diff = correct_weight - wrong_weight
                return 0, weights[c] + diff
        return 0, 0

    _, corrected = helper(name)
    return corrected


@profiler
def part_one(data_input: List[str]) -> str:
    """
    Finds the bottom program name.

    Args:
        data_input (List[str]): Input lines.

    Returns:
        str: Bottom program name.
    """
    _, children = parse_programs(data_input)
    return find_root(children)


@profiler
def part_two(data_input: List[str]) -> int:
    """
    Finds the corrected weight to balance the tower.

    Args:
        data_input (List[str]): Input lines.

    Returns:
        int: Corrected weight.
    """
    weights, children = parse_programs(data_input)
    root = find_root(children)
    return find_unbalance(root, weights, children)


if __name__ == "__main__":
    input_data = get_input("inputs/7_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
