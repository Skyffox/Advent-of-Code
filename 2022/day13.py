# pylint: disable=line-too-long
"""
Part 1: Determine which pairs of packets are already in the right order. What is the sum of the indices of those pairs?
Answer: 5198

Part 2: Organize all of the packets into the correct order. What is the decoder key for the distress signal?
Answer: 22344
"""

from ast import literal_eval
from utils import profiler


def parse_input(file_location):
    """
    The input consists of pairs of packets. Each packet can be a list of integers or nested lists
    I use ast.literal_eval to parse the strings into actual Python objects (like lists or integers)
    """
    with open(file_location, "r", encoding="utf-8") as file:
        return [[literal_eval(line) for line in s.split('\n')] for s in file.read().split('\n\n')]


def compare_item(left, right):
    """
    Compare two lists of integers or nested lists. If both elements being compared are lists, it recurses into those lists.
    Return True if the left is less than the right, else False.
    """
    if isinstance(left, type(right)):
        # Both are lists
        if isinstance(left, list):
            for idx, l in enumerate(left):
                # Right list ran out of indices
                if idx == len(right):
                    return -1
                if compare_item(l, right[idx]) == 1:
                    return 1
                elif compare_item(l, right[idx]) == -1:
                    return -1
            # Left list ran out of indices
            if len(right) > len(left):
                return 1
        # Comparison between numbers
        elif left != right:
            return 1 if left < right else -1
    # If one side is an integer and the other is a list: put the int in a list and compare lists
    else:
        if isinstance(left, int):
            return compare_item([left], right)
        else:
            return compare_item(left, [right])


@profiler
def part_1(pairs):
    """We iterate over all pairs of packets and compare whether they are in the correct order, if they are save the index"""
    return sum(i for i, (pair) in enumerate(pairs, start=1) if compare_item(*pair) == 1)



def flatten(l: list[list[int]]) -> list[int]:
    """Flatten a nested list one level"""
    return [item for sublist in l for item in sublist]


def find_index(l: list[list[int]], item: list[int]) -> int:
    """Return index of where item falls in list"""
    item_idx: int = 0
    for pkt in flatten(l):
        if compare_item(pkt, item) == 1:
            item_idx += 1
    return item_idx


@profiler
def part_2(pairs):
    """Locate the indices of the added divider packets after the signals have been ordered"""
    # Remove one layer of list to match flattened list above
    first_divider: list[int] = [2]
    second_divider: list[int] = [6]

    first_pos: int = find_index(pairs, first_divider) + 1
    second_pos: int = find_index(pairs, second_divider) + 2
    return first_pos * second_pos


if __name__ == "__main__":
    input_data = parse_input("inputs/13_input.txt")

    print(part_1(input_data))
    print(part_2(input_data))
