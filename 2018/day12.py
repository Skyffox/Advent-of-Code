# pylint: disable=line-too-long
"""
Day 12: Subterranean Sustainability

Part 1: After 20 generations, what is the sum of the numbers of all pots which contain a plant?
Answer: 1944

Part 2: After fifty billion (50000000000) generations, what is the sum of the numbers of all pots which contain a plant?
Answer: 250000000219
"""

from typing import Dict, Tuple
from utils import profiler

PADDING = 3  # Number of dots added to both ends to handle edge growth


def get_input(file_path: str) -> Tuple[str, Dict[str, str]]:
    """
    Reads the input file and returns the initial state and rules.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        Tuple[str, dict[str, str]]: The initial state string and the dictionary of rules.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file if line.strip()]

    initial_state = lines[0].split(": ")[1]
    rules = {
        line.split(" => ")[0]: line.split(" => ")[1]
        for line in lines[1:]
    }
    return initial_state, rules


def apply_rules(pots: str, rules: Dict[str, str]) -> str:
    """
    Applies transformation rules to generate the next state of pots.

    Args:
        pots (str): Current state of pots.
        rules (Dict[str, str]): Transformation rules.

    Returns:
        Tuple[int, str]: Offset delta and the next generation's state in canonical form.
    """
    extended = "." * PADDING + pots + "." * PADDING
    next_gen = ["."] * len(extended)

    for pattern, result in rules.items():
        for i in range(len(extended) - 4):
            if extended[i:i + 5] == pattern:
                next_gen[i + 2] = result

    if '#' not in next_gen:
        return 0, '.' # No plants remain

    # Return the offset and the new bounding box (for memory reasons)
    first = next_gen.index('#')
    last = len(next_gen) - 1 - next_gen[::-1].index('#')
    new_pots = ''.join(next_gen[first:last + 1])
    delta = first - PADDING

    return delta, new_pots


@profiler
def solve(pots: str, rules: Dict[str, str], cycles: int) -> int:
    """
    Simulates plant growth and calculates the sum of pot numbers containing plants.

    Args:
        pots (str): Initial state.
        rules (Dict[str, str]): Transformation rules.
        generations (int): Number of generations to simulate.

    Returns:
        int: Final sum of pot numbers containing plants.
    """
    # Determine bounding box of pots
    offset = pots.index('#')
    offset_end = pots.rindex('#')
    pots = pots[offset:offset_end + 1]

    for gen in range(cycles):
        delta, pots_ = apply_rules(pots, rules)

        # Pattern stabilized; extrapolate offset shift
        if pots_ == pots:
            offset += delta * (cycles - gen)
            break

        pots = pots_
        offset += delta

    # Calculates the sum of the numbers of all pots that contain a plant.
    return sum([(i + offset) * (1 if val == '#' else 0) for i, val in enumerate(pots)])


if __name__ == "__main__":
    init_state, pattern = get_input("inputs/12_input.txt")

    print("Part 1:", solve(init_state, pattern, 20))
    print("Part 2:", solve(init_state, pattern, 50_000_000_000))
