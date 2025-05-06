# pylint: disable=line-too-long
"""
Day 3: Crossed Wires

Part 1: Calculate the Manhattan distance from the central port (0, 0) to the closest intersection point.
Answer: 3247

Part 2: Find the fewest combined steps the wires must take to reach an intersection.
Answer: 48054
"""

from typing import List, Tuple, Dict
from utils import profiler


def get_input(file_path: str) -> List[List[Tuple[str, int]]]:
    """
    Parse the input file and return a list of movement instructions for each wire.

    Args:
        file_path (str): Path to the input file.

    Returns:
        List[List[Tuple[str, int]]]: Parsed movement instructions for each wire.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [
            [(move[0], int(move[1:])) for move in line.strip().split(",")]
            for line in file
        ]


def get_path_map(instructions: List[Tuple[str, int]]) -> Dict[Tuple[int, int], int]:
    """
    Generate a path map for a wire, recording the number of steps taken to reach each coordinate.

    Args:
        instructions (List[Tuple[str, int]]): List of movement directions and step counts.

    Returns:
        Dict[Tuple[int, int], int]: Mapping of coordinates to the step count when first reached.
    """
    x, y, steps = 0, 0, 0
    path = {}

    for direction, dist in instructions:
        dx, dy = 0, 0
        if direction == "U":
            dy = 1
        elif direction == "D":
            dy = -1
        elif direction == "L":
            dx = -1
        elif direction == "R":
            dx = 1

        for _ in range(dist):
            x += dx
            y += dy
            steps += 1
            if (x, y) not in path:
                path[(x, y)] = steps

    return path


@profiler
def part_1(wires: List[List[Tuple[str, int]]]) -> int:
    """
    Determine the Manhattan distance from the origin to the closest intersection of the two wires.

    Args:
        wires (List[List[Tuple[str, int]]]): Movement instructions for both wires.

    Returns:
        int: The Manhattan distance of the closest intersection point.
    """
    path1 = get_path_map(wires[0])
    path2 = get_path_map(wires[1])
    intersections = set(path1.keys()) & set(path2.keys())
    return min(abs(x) + abs(y) for x, y in intersections)


@profiler
def part_2(wires: List[List[Tuple[str, int]]]) -> int:
    """
    Determine the fewest combined steps required for both wires to reach an intersection.

    Args:
        wires (List[List[Tuple[str, int]]]): Movement instructions for both wires.

    Returns:
        int: Minimum combined step count to an intersection.
    """
    path1 = get_path_map(wires[0])
    path2 = get_path_map(wires[1])
    intersections = set(path1.keys()) & set(path2.keys())
    return min(path1[pt] + path2[pt] for pt in intersections)


if __name__ == "__main__":
    input_data = get_input("inputs/3_input.txt")
    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
