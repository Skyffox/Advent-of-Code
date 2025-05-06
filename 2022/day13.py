# pylint: disable=line-too-long
"""
Day 13: Distress Signal

Part 1: Determine which pairs of packets are already in the right order. What is the sum of the indices of those pairs?
Answer: 5198

Part 2: Organize all of the packets into the correct order. What is the decoder key for the distress signal?
Answer: 22344
"""

from ast import literal_eval
from typing import List, Tuple
from utils import profiler


def parse_input(file_location: str) -> List[List[List[int]]]:
    """
    Parses the input file containing pairs of packets.

    The input consists of pairs of packets, each being either a list of integers or a nested list.
    This function reads the file, splits the input into pairs, and uses `ast.literal_eval` to parse
    each pair into Python objects (lists of integers or nested lists).

    Args:
        file_location (str): The path to the input file.

    Returns:
        List[List[List[int]]]: A list of pairs of packets, where each packet is a list of integers (or nested lists).
    """
    with open(file_location, "r", encoding="utf-8") as file:
        return [
            [literal_eval(line) for line in s.split('\n')]
            for s in file.read().split('\n\n')
        ]


def compare_item(left: any, right: any) -> int:
    """
    Compares two packets, which may be integers or lists (which may also be nested).
    The function handles recursion for nested lists and compares them element-wise.

    Args:
        left (any): The left element to compare (either an integer or a list).
        right (any): The right element to compare (either an integer or a list).

    Returns:
        int: 1 if `left` is less than `right`, -1 if `left` is greater than `right`, or 0 if they are equal.
    """
    if isinstance(left, type(right)):
        if isinstance(left, list):
            for idx, l in enumerate(left):
                if idx == len(right):
                    return -1  # Right list ran out of indices
                result = compare_item(l, right[idx])
                if result != 0:
                    return result
            if len(right) > len(left):
                return 1  # Left list ran out of indices
        elif left != right:
            return 1 if left < right else -1
    else:
        # One is an integer, the other is a list; wrap the integer in a list and compare
        if isinstance(left, int):
            return compare_item([left], right)
        else:
            return compare_item(left, [right])
    return 0 # They are equal


@profiler
def part_1(pairs: List[Tuple[List[int], List[int]]]) -> int:
    """
    Calculates the sum of the indices of the pairs that are in the correct order.

    For each pair of packets, the function compares them using `compare_item`. If the left packet is 
    less than the right packet, it adds the index of the pair (1-indexed) to the sum.

    Args:
        pairs (List[Tuple[List[int], List[int]]]): A list of pairs of packets.

    Returns:
        int: The sum of the indices of the pairs that are in the correct order.
    """
    return sum(i for i, (left, right) in enumerate(pairs, start=1) if compare_item(left, right) == 1)


def flatten(l: List[List[int]]) -> List[int]:
    """
    Flattens a nested list one level.

    Args:
        l (List[List[int]]): A nested list to flatten.

    Returns:
        List[int]: A flattened list of integers.
    """
    return [item for sublist in l for item in sublist]


def find_index(l: List[List[List[int]]], item: List[int]) -> int:
    """
    Finds the index of the first occurrence of `item` in the list `l`, where `l` is a list of packets.

    Args:
        l (List[List[List[int]]]): A list of packets.
        item (List[int]): The packet to find.

    Returns:
        int: The index where the item falls in the flattened list of packets.
    """
    item_idx = 0
    for pkt in flatten(l):
        if compare_item(pkt, item) == 1:
            item_idx += 1
    return item_idx


@profiler
def part_2(pairs: List[Tuple[List[int], List[int]]]) -> int:
    """
    Finds the decoder key for the distress signal by locating the indices of the divider packets 
    after sorting all the packets.

    Divider packets are represented as `[2]` and `[6]`. The function finds the positions of these 
    divider packets in the ordered list of all packets and computes the decoder key as the product 
    of these two positions.

    Args:
        pairs (List[Tuple[List[int], List[int]]]): A list of pairs of packets.

    Returns:
        int: The decoder key, which is the product of the indices of the divider packets.
    """
    first_divider = [2]
    second_divider = [6]

    first_pos = find_index(pairs, first_divider) + 1
    second_pos = find_index(pairs, second_divider) + 2
    return first_pos * second_pos


if __name__ == "__main__":
    input_data = parse_input("inputs/13_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
