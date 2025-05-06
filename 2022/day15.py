# pylint: disable=line-too-long
"""
Day 15: Beacon Exclusion Zone

Part 1: In the row where y=2000000, how many positions cannot contain a beacon?
Answer: 6078701

Part 2: Find the only possible position for the distress beacon. What is its tuning frequency?
Answer: 12567351400528
"""

from typing import List, Tuple
from utils import profiler


def get_input(file_path: str) -> List[Tuple[Tuple[int, int], int]]:
    """
    Parses the input file and returns a list of sensors and their Manhattan distances to their corresponding beacons.
    The input consists of sensors and beacons, and the Manhattan distance is the sum of the differences in the x and y coordinates.

    Args:
        file_path (str): Path to the input file.

    Returns:
        List[Tuple[Tuple[int, int], int]]: A list of tuples where each tuple contains:
            - Sensor coordinates (x, y).
            - The Manhattan distance between the sensor and its beacon.
    """
    data = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip().split("=")

            sensor = [int(line[1].split(",")[0]), int(line[2].split(":")[0])]
            beacon = [int(line[3].split(",")[0]), int(line[4].split(":")[0])]

            # Calculate the Manhattan distance between the sensor and beacon
            manhattan_distance = abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])

            data.append(((sensor), manhattan_distance))

    return data


def seen_in_row(sensors: List[Tuple[Tuple[int, int], int]], row: int) -> List[Tuple[int, int]]:
    """
    Finds all the horizontal intervals on the given row where beacons cannot be placed based on the sensors' range.

    Args:
        sensors (List[Tuple[Tuple[int, int], int]]): A list of tuples where each tuple contains:
            - Sensor coordinates (x, y).
            - The Manhattan distance from the sensor to the beacon.
        row (int): The y-coordinate of the row where we are checking for beacon placements.

    Returns:
        List[Tuple[int, int]]: A sorted list of tuples, where each tuple represents a range (low, high) where beacons cannot be placed.
    """
    all_edges = []
    for (sx, sy), dist in sensors:
        diff = dist - abs(row - sy)
        if diff >= 0:
            # The range in which beacons cannot be placed
            all_edges.append((sx - diff, sx + diff))

    return sorted(all_edges)


def find_a_hole(edges: List[Tuple[int, int]]) -> int:
    """
    Finds the first gap in a list of intervals representing the sensor ranges.

    Args:
        edges (List[Tuple[int, int]]): A sorted list of tuples representing the sensor ranges on a given row.

    Returns:
        int: The first position where there is a gap in the ranges.
    """
    highest = 0
    for (a, b) in edges:
        if a <= highest + 1:
            highest = max(b, highest)
        else:
            return a - 1


@profiler
def part_1(data: List[Tuple[Tuple[int, int], int]]) -> int:
    """
    Determines how many positions in the row where y = 2000000 cannot contain a beacon.

    Args:
        data (List[Tuple[Tuple[int, int], int]]): The list of sensors and their corresponding Manhattan distances to beacons.

    Returns:
        int: The number of positions in row y=2000000 that cannot contain a beacon.
    """
    limit = 2000000
    x_coors = set()

    for (sx, sy), dist in data:
        # Check if the sensor's range includes this row
        diff = dist - abs(limit - sy)
        if diff >= 0:
            # Add all the x-coordinates where beacons cannot be placed
            for i in range(-diff, diff + 1):
                x = sx + i
                x_coors.add(x)

    return len(x_coors) - 1


@profiler
def part_2(sensors: List[Tuple[Tuple[int, int], int]]) -> int:
    """
    Finds the only possible position for the distress beacon and calculates its tuning frequency.

    Args:
        sensors (List[Tuple[Tuple[int, int], int]]): The list of sensors and their corresponding Manhattan distances to beacons.

    Returns:
        int: The tuning frequency of the distress beacon position.
    """
    limit = 4000000

    for row in reversed(range(limit + 1)):
        edges = seen_in_row(sensors, row)
        if col := find_a_hole(edges):
            # Calculate the tuning frequency for the distress beacon
            return limit * col + row


if __name__ == "__main__":
    input_data = get_input("inputs/15_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
