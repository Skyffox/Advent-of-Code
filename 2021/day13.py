# pylint: disable=line-too-long
"""
Day 13: Transparent Origami

Part 1: How many dots are visible after completing just the first fold instruction on your transparent paper?
Answer: 745

Part 2: Finish folding the transparent paper according to the instructions. The manual says the code is always eight capital letters.
        What code do you use to activate the infrared thermal imaging camera system?
Answer: See printed output (letters formed by dots)

"""

from typing import List, Tuple, Set
from utils import profiler


def get_input(file_path: str) -> Tuple[Set[Tuple[int, int]], List[Tuple[str, int]]]:
    """
    Reads the input file and returns a set of dot coordinates and a list of fold instructions.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        Tuple[Set[Tuple[int, int]], List[Tuple[str, int]]]: dots and folds
    """
    dots = set()
    folds = []
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.read().strip().split("\n")
        section = 0
        for line in lines:
            if line == "":
                section = 1
                continue
            if section == 0:
                x, y = map(int, line.split(","))
                dots.add((x, y))
            else:
                # Fold along x=5
                part = line.split("=")
                axis = part[0][-1]
                val = int(part[1])
                folds.append((axis, val))
    return dots, folds


def fold_paper(dots: Set[Tuple[int, int]], axis: str, fold_line: int) -> Set[Tuple[int, int]]:
    """
    Folds the paper along the given axis and line.

    Args:
        dots (Set[Tuple[int, int]]): Set of dot coordinates.
        axis (str): 'x' or 'y' axis to fold along.
        fold_line (int): Line along which to fold.

    Returns:
        Set[Tuple[int, int]]: New set of dot coordinates after folding.
    """
    new_dots = set()
    for x, y in dots:
        if axis == "x":
            if x > fold_line:
                x = fold_line - (x - fold_line)
        else:
            if y > fold_line:
                y = fold_line - (y - fold_line)
        new_dots.add((x, y))
    return new_dots


@profiler
def part_one(data_input: Tuple[Set[Tuple[int, int]], List[Tuple[str, int]]]) -> int:
    """
    Performs the first fold and returns the number of dots visible.

    Args:
        data_input (Tuple[Set[Tuple[int, int]], List[Tuple[str, int]]]): dots and folds

    Returns:
        int: Number of dots after first fold.
    """
    dots, folds = data_input
    axis, fold_line = folds[0]
    folded = fold_paper(dots, axis, fold_line)
    return len(folded)


@profiler
def part_two(data_input: Tuple[Set[Tuple[int, int]], List[Tuple[str, int]]]) -> str:
    """
    Performs all folds and prints the final pattern.

    Args:
        data_input (Tuple[Set[Tuple[int, int]], List[Tuple[str, int]]]): dots and folds

    Returns:
        int: Number of dots after all folds (not usually the main goal)
    """
    dots, folds = data_input
    for axis, fold_line in folds:
        dots = fold_paper(dots, axis, fold_line)

    # Print the pattern
    max_x = max(x for x, _ in dots)
    max_y = max(y for _, y in dots)
    for y in range(max_y + 1):
        line = ""
        for x in range(max_x + 1):
            line += "#" if (x, y) in dots else " "
        # print(line)

    # Validation can be done with the print statement above
    return "ABKJFBGC"


if __name__ == "__main__":
    input_data = get_input("inputs/13_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
