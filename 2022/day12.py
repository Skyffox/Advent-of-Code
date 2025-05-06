# pylint: disable=line-too-long
"""
Day 12: Hill Climbing Algorithm

Part 1: What is the fewest steps required to move from your current position to the location that should get the best signal?
Answer: 370

Part 2: What is the fewest steps required to move starting from any square with elevation `a` to the location that should get the best signal?
Answer: 363
"""

from typing import List, Tuple, Optional
from utils import profiler


def get_input(file_name: str) -> Tuple[List[List[int]], Tuple[int, int], Tuple[int, int]]:
    """
    Reads the grid from the input file and locates the source ('S') and target ('E') positions.

    The grid consists of lowercase letters where 'S' is treated as elevation 0, and 'E' as elevation 25. 
    The function returns the grid along with the source and target positions.

    Args:
        file_name (str): The name of the input file containing the grid.

    Returns:
        Tuple[List[List[int]], Tuple[int, int], Tuple[int, int]]: 
            A tuple containing:
            - A 2D list representing the elevation grid.
            - A tuple (x, y) representing the source's position.
            - A tuple (x, y) representing the target's position.
    """
    grid = []
    source, target = None, None
    with open(file_name, "r", encoding="utf-8") as file:
        for i, line in enumerate(file):
            row = []
            for j, char in enumerate(line.strip()):
                if char == 'S':
                    source = (j, i)
                    row.append(0)
                elif char == 'E':
                    target = (j, i)
                    row.append(25)
                else:
                    row.append(ord(char) - ord('a'))
            grid.append(row)

    return grid, source, target


def validate_move(grid: List[List[int]], x: int, y: int, elevation: int) -> bool:
    """
    Validates if the move to the given coordinates is within the grid and the elevation difference 
    is within an acceptable range (not steeper than a climb of 1).

    Args:
        grid (List[List[int]]): The elevation grid.
        x (int): The x-coordinate of the potential move.
        y (int): The y-coordinate of the potential move.
        elevation (int): The current elevation (height) from where the move is being made.

    Returns:
        bool: True if the move is valid, False otherwise.
    """
    x_range, y_range = range(len(grid[0])), range(len(grid))
    return (x in x_range) and (y in y_range) and (grid[y][x] <= elevation + 1)


def navigate(grid: List[List[int]], source: Tuple[int, int], target: Tuple[int, int]) -> Optional[int]:
    """
    Finds the shortest path from the source to the target in the elevation grid using a breadth-first search.

    The search ensures that each move does not exceed a climb of 1 in elevation.

    Args:
        grid (List[List[int]]): The elevation grid.
        source (Tuple[int, int]): The starting position (x, y) of the source.
        target (Tuple[int, int]): The target position (x, y).

    Returns:
        Optional[int]: The number of steps required to reach the target, or None if no valid path exists.
    """
    steps = 0
    elevation = 0
    visited = {source: (steps, elevation)}
    queue = [source]

    while queue:
        x, y = queue.pop(0)
        steps, elevation = visited[(x, y)]

        if (x, y) == target:
            return steps

        # Possible moves (right, left, down, up)
        moves = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        possible_moves = [(nx, ny) for nx, ny in moves if validate_move(grid, nx, ny, elevation)]

        for nx, ny in possible_moves:
            if (nx, ny) not in visited:
                visited[(nx, ny)] = (steps + 1, grid[ny][nx])
                queue.append((nx, ny))

    return None


@profiler
def part_1(grid: List[List[int]], source: Tuple[int, int], target: Tuple[int, int]) -> int:
    """
    Solves Part 1 of the problem by finding the shortest path from the source to the target in the grid.

    Args:
        grid (List[List[int]]): The elevation grid.
        source (Tuple[int, int]): The source position.
        target (Tuple[int, int]): The target position.

    Returns:
        int: The number of steps required to reach the target.
    """
    return navigate(grid, source, target)


@profiler
def part_2(grid: List[List[int]], target: Tuple[int, int]) -> int:
    """
    Solves Part 2 of the problem by finding the shortest path from any position with elevation 0 (starting points) 
    to the target.

    Args:
        grid (List[List[int]]): The elevation grid.
        target (Tuple[int, int]): The target position.

    Returns:
        int: The minimum number of steps required to reach the target from any possible starting position with elevation 0.
    """
    possible_starts = [(x, y) for y, row in enumerate(grid) for x, elevation in enumerate(row) if elevation == 0]
    return min(filter(lambda x: x is not None, [navigate(grid, source, target) for source in possible_starts]))


if __name__ == "__main__":
    elevations, start, end = get_input("inputs/12_input.txt")

    print(f"Part 1: {part_1(elevations, start, end)}")
    print(f"Part 2: {part_2(elevations, end)}")
