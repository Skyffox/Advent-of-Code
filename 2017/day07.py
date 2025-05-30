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


def get_input(file_path: str) -> Tuple[Dict[str, int], Dict[str, List[str]]]:
    """
    Reads and parses the input file to extract program weights and their children.

    Each line has the format:
        program_name (weight) -> child1, child2, ...
    or
        program_name (weight)

    Args:
        file_path (str): Path to the input text file.

    Returns:
        Tuple:
            weights (Dict[str, int]): Mapping of program name to its weight.
            children (Dict[str, List[str]]): Mapping of program name to list of children.
    """
    weights, children = {}, {}
    pattern = re.compile(r"(\w+)\s+\((\d+)\)(?:\s+->\s+([\w\s,]+))?")
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            match = pattern.match(line.strip())
            if match:
                name, weight, kids = match.groups()
                weights[name] = int(weight)
                children[name] = [k.strip() for k in kids.split(",")] if kids else []
    return weights, children


def find_root(children: Dict[str, List[str]]) -> str:
    """
    Finds the root program — the one that is not anyone's child.

    Args:
        children (Dict[str, List[str]]): Mapping of program names to their children.

    Returns:
        str: Name of the root program.
    """
    all_nodes = set(children.keys())
    child_nodes = {c for kids in children.values() for c in kids}
    root = list(all_nodes - child_nodes)[0]
    return root


@profiler
def part_one(data: Tuple[Dict[str, int], Dict[str, List[str]]]) -> str:
    """
    Identifies the bottom program (root) of the tower.

    Args:
        data (Tuple): Parsed input consisting of:
            - weights: Mapping of program names to their weights.
            - children: Mapping of program names to list of children.

    Returns:
        str: The name of the bottom program.
    """
    _, children = data
    return find_root(children)


@profiler
def part_two(data: Tuple[Dict[str, int], Dict[str, List[str]]]) -> int:
    """
    Determines the corrected weight of the single unbalanced program to balance the entire tower.

    Uses recursion and memoization to:
    - Compute total weights of each subtree.
    - Detect imbalance among siblings.
    - Calculate required weight adjustment for the unbalanced program.

    Args:
        data (Tuple): Parsed input consisting of:
            - weights: Mapping of program names to their weights.
            - children: Mapping of program names to list of children.

    Returns:
        int: The corrected weight to balance the tower.
    """
    weights, children = data
    root = find_root(children)
    memo = {}

    def compute_weight(name: str) -> int:
        """
        Recursively compute total weight of a program including its children.

        Uses memoization to avoid redundant computations.
        """
        if name in memo:
            return memo[name]
        total = weights[name] + sum(compute_weight(c) for c in children[name])
        memo[name] = total
        return total

    def find_unbalance(node: str) -> int:
        """
        Recursively traverses the tower to find the unbalanced program.

        Steps:
        1. Compute total weights of all children.
        2. Count occurrences of each child's total weight.
        3. If all weights match, this node is balanced; return 0.
        4. Otherwise, identify the unique (wrong) weight and the correct weight.
        5. Recursively check which child has the wrong weight.
        6. When the unbalanced program is found, calculate the corrected weight
           by adjusting it based on the difference between correct and wrong weights.
        """
        child_weights = [compute_weight(c) for c in children[node]]
        # Count how many children have each weight
        weight_counts = {}
        for w in child_weights:
            weight_counts[w] = weight_counts.get(w, 0) + 1

        # If all children have the same total weight, this node is balanced
        if len(weight_counts) <= 1:
            return 0 # balanced, no correction needed here

        # Identify the correct weight (the one appearing most often)
        correct_weight = max(weight_counts, key=weight_counts.get)
        # Identify the wrong weight (the one appearing least often)
        wrong_weight = min(weight_counts, key=weight_counts.get)

        # Find which child has the wrong weight and check deeper
        for c, w in zip(children[node], child_weights):
            if w == wrong_weight:
                # Recurse down to see if the imbalance is deeper
                correction = find_unbalance(c)
                if correction != 0:
                    return correction # found deeper unbalance, propagate up
                # Calculate and return the corrected weight for the unbalanced program
                diff = correct_weight - wrong_weight
                return weights[c] + diff

        return 0 # fallback, should never reach here if tree is unbalanced

    return find_unbalance(root)


if __name__ == "__main__":
    input_data = get_input("inputs/7_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
