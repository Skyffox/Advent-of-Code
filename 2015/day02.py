# pylint: disable=line-too-long
"""
Day 2: I Was Told There Would Be No Math

Part 1: How much wrapping paper is needed for a present with certain dimensions
Answer: 1588178

Part 2: The elves want a ribbon to wrap the present, calculate how much feet they need
Answer: 3783758
"""

from typing import Tuple, List
from utils import profiler


def get_input(file_path: str) -> Tuple[List[int], List[int], List[int]]:
    """
    Parses the input file and extracts dimensions of each present.

    Args:
        file_path (str): Path to the input file.

    Returns:
        Tuple[List[int], List[int], List[int]]: Lists of widths, lengths, and heights.
    """
    widths, lengths, heights = [], [], []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            l, w, h = map(int, line.strip().split("x"))
            lengths.append(l)
            widths.append(w)
            heights.append(h)

    return widths, lengths, heights


@profiler
def part_1(widths: List[int], lengths: List[int], heights: List[int]) -> int:
    """
    Calculates the total amount of wrapping paper needed.

    Args:
        widths (List[int]): List of present widths.
        lengths (List[int]): List of present lengths.
        heights (List[int]): List of present heights.

    Returns:
        int: Total square feet of wrapping paper required.
    """
    total = 0
    for idx, w_item in enumerate(widths):
        side_1 = lengths[idx] * w_item
        side_2 = w_item * heights[idx]
        side_3 = heights[idx] * lengths[idx]
        smallest_side = min(side_1, side_2, side_3)

        total += 2 * side_1 + 2 * side_2 + 2 * side_3 + smallest_side

    return total


@profiler
def part_2(widths: List[int], lengths: List[int], heights: List[int]) -> int:
    """
    Calculates the total amount of ribbon required.

    Ribbon = smallest perimeter of any one face + volume of the box.

    Args:
        widths (List[int]): List of present widths.
        lengths (List[int]): List of present lengths.
        heights (List[int]): List of present heights.

    Returns:
        int: Total feet of ribbon required.
    """
    total = 0
    for i, w in enumerate(widths):
        dimensions = sorted([w, lengths[i], heights[i]])
        perimeter = 2 * (dimensions[0] + dimensions[1])
        bow = dimensions[0] * dimensions[1] * dimensions[2]
        total += perimeter + bow

    return total


if __name__ == "__main__":
    width, length, height = get_input("inputs/2_input.txt")

    print(f"Part 1: {part_1(width, length, height)}")
    print(f"Part 2: {part_2(width, length, height)}")
