# pylint: disable=line-too-long
"""
Day 8 Challenge: Playground 

Part 1: String lines between junction boxes (your input) connect together the 1000 pairs of junction boxes which are closest together. 
Then multiply together the sizes of the three largest circuits.
Answer: 29406

Part 2: Continue connecting the closest unconnected pairs of junction boxes together until they're all in the same circuit. 
Then multiply together the X coordinates of the last two junction boxes you need to connect.
Answer: 7499461416
"""

import math
from typing import List, Tuple
from utils import profiler


def get_input(file_path: str) -> List[List[int]]:
    """
    Load the list of 3D junction box coordinates from the puzzle input file.

    For example:
        162,817,812
        57,618,57
        906,360,560
        ...

    This function reads the file, parses every line into a list of integers,
    and returns a list of all junction box coordinates.

    Args:
        file_path (str): Path to the input text file containing junction
            box coordinate data.

    Returns:
        List[List[int]]: A list of [X, Y, Z] coordinate triplets.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [list(map(int, line.strip().split(","))) for line in file]


def straight_line_distance(point_a: List[int], point_b: List[int]) -> float:
    """
    Compute the Euclidean distance between two coordinate points.

    Args:
        point_a (List[int]): First coordinate, e.g., [x, y, z].
        point_b (List[int]): Second coordinate, e.g., [x, y, z].

    Returns:
        float: The Euclidean distance between the two points.
    """
    return sum((a - b) ** 2 for a, b in zip(point_a, point_b)) ** 0.5


def build_distance_pairs(coords: List[List[int]]) -> List[Tuple[float, List[int], List[int]]]:
    """
    Compute all pairwise distances between coordinates.

    Args:
        coords (List[List[int]]): A list of coordinate pairs.

    Returns:
        List[Tuple[float, List[int], List[int]]]:
            Sorted list of (distance, pointA, pointB).
    """
    distance_pairs = []
    for idx, point_a in enumerate(coords):
        for point_b in coords[idx+1:]:
            dist = straight_line_distance(point_a, point_b)
            distance_pairs.append((dist, point_a, point_b))

    return sorted(distance_pairs, key=lambda x: x[0])


def merge_groups(groups: List[List[List[int]]], p1: List[int], p2: List[int]):
    """
    Merge or create groups based on two points that share a connection.

    Args:
        groups (List[List[List[int]]]): Existing groups of connected points.
        p1 (List[int]): First point.
        p2 (List[int]): Second point.

    Returns:
        None (groups are modified in-place)
    """
    matching_groups = [g for g in groups if p1 in g or p2 in g]

    if not matching_groups:
        # Neither point is in an existing group, create a new group
        groups.append([p1, p2])

    elif len(matching_groups) == 1:
        # One group found, extend it
        group = matching_groups[0]
        if p1 not in group:
            group.append(p1)
        if p2 not in group:
            group.append(p2)

    else:
        # Points are in separate groups, merge them
        group_a, group_b = matching_groups
        if group_a is not group_b:
            group_a.extend([pt for pt in group_b if pt not in group_a])
            groups.remove(group_b)


@profiler
def part_one(coords: List[List[int]]) -> int:
    """
    Form connection groups based on the shortest distances and
    return the product of the sizes of the three largest groups.

    Args:
        coords (List[List[int]]): List of coordinate pairs.

    Returns:
        int: Product of the sizes of the three largest groups.
    """
    distance_list = build_distance_pairs(coords)
    groups: List[List[List[int]]] = []

    for _, p1, p2 in distance_list[:1000]:
        merge_groups(groups, p1, p2)

    # Get the three largest subgroups
    return math.prod(len(group) for group in sorted(groups, key=len, reverse=True)[:3])


@profiler
def part_two(coords: List[List[int]]) -> int:
    """
    Connect coordinates in increasing distance order until all are part of the same cluster
    Return the product of the X-values of the edge that completes the full connection.

    Args:
        coords (List[List[int]]): List of coordinate pairs.

    Returns:
        int: Product of the x-coordinates of the final linking edge.
    """
    distance_list = build_distance_pairs(coords)
    groups: List[List[List[int]]] = []
    final_edge: Tuple[List[int], List[int]] | None = None

    for _, p1, p2 in distance_list:
        merge_groups(groups, p1, p2)
        final_edge = (p1, p2)

        # Stop if all points are in one group
        if len(groups) == 1 and len(groups[0]) == len(coords):
            break

    return final_edge[0][0] * final_edge[1][0]


if __name__ == "__main__":
    # Get input data
    input_data = get_input("inputs/8_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
