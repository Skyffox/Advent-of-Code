# pylint: disable=line-too-long
"""
Day 9: Mirage Maintenance

Part 1: Find the sum of extrapolated values that would come next in the series.
Answer: 2043677056

Part 2: Find the sum of extrapolated values that would precede the series.
Answer: 1062
"""

from typing import List, Tuple
from utils import profiler


def get_input(file_path: str) -> List[List[int]]:
    """
    Reads the input data from a file and converts it into a list of integer lists.

    Args:
        file_path (str): The path to the input file containing the series.

    Returns:
        List[List[int]]: A list of lists, where each inner list contains integers parsed from a line in the file.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [list(map(int, line.strip().split())) for line in file]


def differences(lst: List[int]) -> List[int]:
    """
    Calculates the differences between consecutive elements in a list.

    Args:
        lst (List[int]): A list of integers.

    Returns:
        List[int]: A list of differences between each consecutive pair of integers in the input list.
    """
    return [lst[i + 1] - lst[i] for i in range(len(lst) - 1)]


@profiler
def compute(sequences: List[List[int]]) -> Tuple[int, int]:
    """
    Computes the sum of extrapolated values that would come next (Part 1)
    and the sum of values that would precede the series (Part 2).

    For each input sequence, the function builds a pyramid of difference layers until a layer
    contains only zeros. It then extrapolates the next and previous values in the sequence
    using these differences.

    Args:
        sequences (List[List[int]]): A list of integer sequences.

    Returns:
        Tuple[int, int]: A tuple containing:
            - The sum of all next extrapolated values (Part 1).
            - The sum of all previous extrapolated values (Part 2).
    """
    total_part1 = 0
    total_part2 = 0

    for line in sequences:
        layers = [line[:]]

        # Build difference layers until all elements are zero
        while any(layers[-1]):
            layers.append(differences(layers[-1]))

        # Extrapolate the next value
        diff = 0
        for layer in reversed(layers):
            layer.append(layer[-1] + diff)
            diff = layer[-1]

        total_part1 += layers[0][-1]

        # Extrapolate the previous value
        diff = 0
        for layer in reversed(layers):
            layer.insert(0, layer[0] - diff)
            diff = layer[0]

        total_part2 += layers[0][0]

    return total_part1, total_part2


if __name__ == "__main__":
    input_data = get_input("inputs/9_input.txt")
    ans_part1, ans_part2 = compute(input_data)

    print(f"Part 1: {ans_part1}")
    print(f"Part 2: {ans_part2}")
