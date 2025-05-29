# pylint: disable=line-too-long
"""
Day 15: Oxygen System

Part 1: What is the fewest number of movement commands required to move the repair droid from its starting position to the location of the oxygen system?
Answer: 230

Part 2: Use the repair droid to get a complete map of the area. How many minutes will it take to fill with oxygen?
Answer: 288
"""

from typing import List, Tuple, Dict
from collections import deque
from utils import IntcodeComputer
from utils import profiler


def get_input(file_path: str) -> List[int]:
    """
    Reads the input file and returns the Intcode program as a list of integers.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        List[int]: The Intcode program.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return list(map(int, file.read().strip().split(",")))


DIRECTIONS = {
    1: (0, -1),  # North
    2: (0, 1),   # South
    3: (-1, 0),  # West
    4: (1, 0),   # East
}


def bfs_explore(program: List[int]) -> Tuple[Dict[Tuple[int, int], int], Tuple[int, int]]:
    """
    Explore the map using BFS controlling the Intcode droid.

    Returns:
        Tuple:
            - map of positions to tile type (0=wall, 1=empty, 2=oxygen system)
            - position of oxygen system
    """
    computer = IntcodeComputer(program)
    start = (0, 0)
    visited = {start: 1}
    queue = deque([(start, computer)])
    oxygen_pos = None

    while queue:
        pos, comp = queue.popleft()
        for direction, (dx, dy) in DIRECTIONS.items():
            new_pos = (pos[0] + dx, pos[1] + dy)
            if new_pos in visited:
                continue

            new_comp = comp.copy()
            new_comp.add_input(direction)
            status = new_comp.run()

            visited[new_pos] = status
            if status == 0:
                continue
            if status == 2:
                oxygen_pos = new_pos
            queue.append((new_pos, new_comp))

    return visited, oxygen_pos


def bfs_shortest_path(visited: Dict[Tuple[int, int], int], start: Tuple[int, int], target: Tuple[int, int]) -> int:
    """
    BFS to find shortest path length between start and target in the map.

    Args:
        visited (Dict[Tuple[int, int], int]): Map of positions to tile types.
        start (Tuple[int, int]): Start position.
        target (Tuple[int, int]): Target position.

    Returns:
        int: Shortest path length.
    """
    queue = deque([(start, 0)])
    seen = {start}

    while queue:
        pos, dist = queue.popleft()
        if pos == target:
            return dist

        for dx, dy in DIRECTIONS.values():
            new_pos = (pos[0] + dx, pos[1] + dy)
            if new_pos in visited and visited[new_pos] != 0 and new_pos not in seen:
                seen.add(new_pos)
                queue.append((new_pos, dist + 1))

    return -1


def bfs_fill_oxygen(visited: Dict[Tuple[int, int], int], start: Tuple[int, int]) -> int:
    """
    BFS to find time to fill entire area with oxygen.

    Args:
        visited (Dict[Tuple[int, int], int]): Map of positions to tile types.
        start (Tuple[int, int]): Oxygen system position.

    Returns:
        int: Minutes to fill with oxygen.
    """
    queue = deque([(start, 0)])
    seen = {start}
    max_dist = 0

    while queue:
        pos, dist = queue.popleft()
        max_dist = max(max_dist, dist)
        for dx, dy in DIRECTIONS.values():
            new_pos = (pos[0] + dx, pos[1] + dy)
            if new_pos in visited and visited[new_pos] != 0 and new_pos not in seen:
                seen.add(new_pos)
                queue.append((new_pos, dist + 1))

    return max_dist


@profiler
def part_one(data_input: List[int]) -> int:
    """
    Finds shortest path to oxygen system.

    Args:
        data_input (List[int]): Intcode program.

    Returns:
        int: Number of steps to oxygen system.
    """
    visited, oxygen_pos = bfs_explore(data_input)
    return bfs_shortest_path(visited, (0, 0), oxygen_pos)


@profiler
def part_two(data_input: List[int]) -> int:
    """
    Finds minutes to fill area with oxygen.

    Args:
        data_input (List[int]): Intcode program.

    Returns:
        int: Minutes to fill with oxygen.
    """
    visited, oxygen_pos = bfs_explore(data_input)
    return bfs_fill_oxygen(visited, oxygen_pos)


if __name__ == "__main__":
    input_data = get_input("inputs/15_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
