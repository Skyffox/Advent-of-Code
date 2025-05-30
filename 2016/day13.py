# pylint: disable=line-too-long
"""
Day 13: A Maze of Twisty Little Cubicles

Part 1: What is the fewest number of steps required for you to reach 31,39?
Answer: 92

Part 2: How many locations (distinct x,y coordinates, including your starting location) can you reach in at most 50 steps?
Answer: 124
"""

from typing import List, Tuple, Set
from collections import deque
from utils import profiler


def get_input(file_path: str) -> List[str]:
    """
    Reads the input file and returns a list with the favorite number as a single integer string.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        List[str]: List containing one string - the favorite number.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file]


def is_open(x: int, y: int, favorite_number: int) -> bool:
    """
    Determines if the coordinate (x,y) is an open space or a wall.

    Args:
        x (int): x-coordinate.
        y (int): y-coordinate.
        favorite_number (int): The office designer's favorite number.

    Returns:
        bool: True if open space, False if wall.
    """
    if x < 0 or y < 0:
        return False
    val = x * x + 3 * x + 2 * x * y + y + y * y + favorite_number
    bits = bin(val).count('1')
    return bits % 2 == 0


@profiler
def part_one(data_input: List[str]) -> int:
    """
    Computes the shortest path from the starting coordinate (1, 1) 
    to the target coordinate (31, 39) on a grid defined by a "favorite number".
    
    The grid consists of open spaces and walls determined by the formula:
    A coordinate is open if the number of 1-bits in a certain calculation is even.
    
    Uses a breadth-first search (BFS) to explore reachable positions, ensuring
    the minimal number of steps is found to reach the target.
    
    Args:
        data_input (List[str]): List with a single string representing the favorite number.
    
    Returns:
        int: The minimum number of steps required to reach the target coordinate (31, 39).
             Returns -1 if the target is unreachable.
    """
    favorite_number = int(data_input[0])
    target = (31, 39)
    queue = deque()
    queue.append((1, 1, 0)) # Start at coordinate (1,1) with 0 steps taken
    visited: Set[Tuple[int, int]] = set()
    visited.add((1, 1))

    while queue:
        x, y, steps = queue.popleft()

        # Check if we have reached the target coordinate
        if (x, y) == target:
            return steps

        # Explore neighboring positions (up, down, left, right)
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            nx, ny = x + dx, y + dy

            # Only consider positions not yet visited and that are "open" spaces
            if (nx, ny) not in visited and is_open(nx, ny, favorite_number):
                visited.add((nx, ny))
                queue.append((nx, ny, steps + 1))

    # Target is unreachable if the queue is exhausted without finding it
    return -1


@profiler
def part_two(data_input: List[str]) -> int:
    """
    Counts the number of distinct locations reachable from (1, 1) within 50 steps,
    on the grid defined by the "favorite number".
    
    Uses a breadth-first search (BFS) to explore all reachable positions, tracking
    how many unique positions can be visited without exceeding 50 steps.
    
    Args:
        data_input (List[str]): List with a single string representing the favorite number.
    
    Returns:
        int: The total number of unique locations reachable in at most 50 steps.
    """
    favorite_number = int(data_input[0])
    queue = deque()
    queue.append((1, 1, 0))  # Starting position and step count
    visited: Set[Tuple[int, int]] = set()
    visited.add((1, 1))

    while queue:
        x, y, steps = queue.popleft()

        # If we've reached the step limit, don't explore further from this position
        if steps == 50:
            continue

        # Explore adjacent positions
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            nx, ny = x + dx, y + dy

            # Only enqueue positions that are open and not visited yet
            if (nx, ny) not in visited and is_open(nx, ny, favorite_number):
                visited.add((nx, ny))
                queue.append((nx, ny, steps + 1))

    # The visited set contains all unique reachable positions within 50 steps
    return len(visited)


if __name__ == "__main__":
    input_data = get_input("inputs/13_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
