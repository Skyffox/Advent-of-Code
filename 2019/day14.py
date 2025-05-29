# pylint: disable=line-too-long
"""
Day 14: Space Stoichiometry

Part 1: Given the list of reactions in your puzzle input, what is the minimum amount of ORE required to produce exactly 1 FUEL?
Answer: 1185296

Part 2: Given 1 trillion ORE, what is the maximum amount of FUEL you can produce?
Answer: 1376631
"""

import math
from typing import List, Dict, Tuple
from collections import defaultdict
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
        return [line.strip() for line in file if line.strip()]


def parse_reactions(data_input: List[str]) -> Dict[str, Tuple[int, List[Tuple[int, str]]]]:
    """
    Parses reaction rules into a dictionary.

    Returns:
        Dict[str, Tuple[int, List[Tuple[int, str]]]]: Maps chemical output to (amount produced, [(input_amount, input_chemical), ...])
    """
    reactions = {}
    for line in data_input:
        inputs_part, output_part = line.split(" => ")
        output_amount, output_chem = output_part.split()
        inputs = []
        for inp in inputs_part.split(", "):
            amt, chem = inp.split()
            inputs.append((int(amt), chem))
        reactions[output_chem] = (int(output_amount), inputs)
    return reactions


def ore_required(reactions: Dict[str, Tuple[int, List[Tuple[int, str]]]], fuel_amount: int) -> int:
    """
    Calculates how much ORE is needed to produce the given amount of FUEL.

    Args:
        reactions (Dict[str, Tuple[int, List[Tuple[int, str]]]]): Reaction rules.
        fuel_amount (int): Amount of FUEL to produce.

    Returns:
        int: Amount of ORE required.
    """
    need = defaultdict(int)
    need["FUEL"] = fuel_amount # Start by needing the desired amount of FUEL
    leftovers = defaultdict(int) # Track leftover chemicals after reactions

    while True:
        # Find a chemical to process that's not ORE and needed > 0
        chem = next((c for c in need if c != "ORE" and need[c] > 0), None)
        # No more chemicals needed except ORE, we are done
        if chem is None:
            break

        qty_needed = need[chem]

        # Use any leftover amount of this chemical before producing more
        if leftovers[chem]:
            used = min(leftovers[chem], qty_needed)
            leftovers[chem] -= used
            qty_needed -= used
        # Leftovers satisfied the need, no new production required
        if qty_needed == 0:
            need[chem] = 0
            continue

        # Calculate how many times to run the reaction to meet or exceed qty_needed
        output_qty, inputs = reactions[chem]
        times = math.ceil(qty_needed / output_qty)

        # Update leftovers: produced more than needed, so leftover is stored
        leftovers[chem] += times * output_qty - qty_needed
        # Mark that we no longer need this chemical (need fulfilled)
        need[chem] = 0

        # Add the input chemicals required for these reaction runs to the need list
        for amt, c in inputs:
            need[c] += amt * times

    # After all processing, need["ORE"] contains the total raw ORE required
    return need["ORE"]


@profiler
def part_one(data_input: List[str]) -> int:

    """
    Solves part one: How much ORE needed for 1 FUEL.

    Args:
        data_input (List[str]): Input reaction rules.

    Returns:
        int: ORE required for 1 FUEL.
    """
    reactions = parse_reactions(data_input)
    return ore_required(reactions, 1)


@profiler
def part_two(data_input: List[str]) -> int:
    """
    Solves part two: Max FUEL producible with 1 trillion ORE.

    Args:
        data_input (List[str]): Input reaction rules.

    Returns:
        int: Maximum FUEL producible.
    """
    reactions = parse_reactions(data_input)
    trillion = 1_000_000_000_000

    low, high = 1, trillion
    while low < high:
        mid = (low + high + 1) // 2
        required = ore_required(reactions, mid)
        if required <= trillion:
            low = mid
        else:
            high = mid - 1
    return low


if __name__ == "__main__":
    input_data = get_input("inputs/14_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
