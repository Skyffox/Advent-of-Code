# pylint: disable=line-too-long
"""
Day 3: No Matter How You Slice It

Part 1: Determine how many square inches of fabric are within two or more claims.  
Answer: 118322

Part 2: Identify the single claim that does not overlap with any others.  
Answer: 1178
"""

from typing import List, Tuple, Dict
from utils import profiler


def get_input(file_path: str) -> List[Tuple[int, int, int, int, str]]:
    """
    Parses the input file and extracts fabric claims.

    Each line has the format: #ID @ X,Y: WxH

    Args:
        file_path (str): Path to the input file.

    Returns:
        List[Tuple[int, int, int, int, str]]: A list of tuples containing (x_start, y_start, width, height, id).
    """
    claims = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split()
            claim_id = parts[0][1:]
            x_start = int(parts[2].split(",")[0])
            y_start = int(parts[2].split(",")[1][:-1])
            width, height = map(int, parts[3].split("x"))
            claims.append((x_start, y_start, width, height, claim_id))
    return claims


@profiler
def part_1(claims: List[Tuple[int, int, int, int, str]]) -> Tuple[int, Dict[Tuple[int, int], int]]:
    """
    Counts how many square inches are covered by two or more claims.

    Args:
        claims (List): List of fabric claims.

    Returns:
        Tuple[int, dict]: The number of overlapping inches and the populated grid dictionary.
    """
    grid = {}
    for x_start, y_start, width, height, _ in claims:
        for x in range(x_start, x_start + width):
            for y in range(y_start, y_start + height):
                grid[(x, y)] = grid.get((x, y), 0) + 1

    overlap_count = sum(1 for count in grid.values() if count > 1)
    return overlap_count, grid


@profiler
def part_2(claims: List[Tuple[int, int, int, int, str]], grid: Dict[Tuple[int, int], int]) -> str:
    """
    Finds the claim that does not overlap with any other.

    Args:
        claims (List): List of fabric claims.
        grid (dict): Dictionary of fabric square counts.

    Returns:
        str: The claim ID with no overlaps.
    """
    for x_start, y_start, width, height, claim_id in claims:
        if all(grid[(x, y)] == 1 for x in range(x_start, x_start + width) for y in range(y_start, y_start + height)):
            return claim_id

    return ""


if __name__ == "__main__":
    input_data = get_input("inputs/3_input.txt")
    overlaps, fabric_grid = part_1(input_data)

    print(f"Part 1: {overlaps}")
    print(f"Part 2: {part_2(input_data, fabric_grid)}")
