# pylint: disable=line-too-long
"""
Day 17: Clumsy Crucible

Part 1: Directing the crucible from the lava pool to the machine parts factory, but not moving more than three consecutive blocks in the same direction,
        what is the least heat loss it can incur?
Answer: 638

Part 2: Directing the ultra crucible from the lava pool to the machine parts factory, which requires moving a minimum of four blocks in the same direction before turning,
        and can move a maximum of ten consecutive blocks without turning, what is the least heat loss it can incur?
Answer: 748
"""

import sys
import heapq
from enum import Enum
from collections import defaultdict
from utils import profiler


class Direction(Enum):
    """
    Enum class to represent the four possible directions in a 2D grid or plane.

    The directions are represented as tuples, where each tuple consists of 
    the change in the x (horizontal) and y (vertical) coordinates.
    """
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


# Define allowed turns for the crucible from each direction
ALLOWED_CRUCIBLE_TURNS = {
    Direction.RIGHT: [Direction.UP, Direction.DOWN],
    Direction.LEFT: [Direction.UP, Direction.DOWN],
    Direction.UP: [Direction.LEFT, Direction.RIGHT],
    Direction.DOWN: [Direction.LEFT, Direction.RIGHT],
}


def get_input(file_path: str) -> list[list[int]]:
    """
    Reads and parses the input data into a 2D grid of integers.

    Args:
        file_path (str): The path to the input file.

    Returns:
        list[list[int]]: A 2D list representing the grid, where each element is an integer.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [[int(x) for x in line.strip()] for line in file]


@profiler
def compute(grid: list[list[int]], blocks_before_turn: int, max_in_direction: int) -> int:
    """
    Finds the minimum heat loss path using Dijkstra's algorithm with a priority queue.

    Args:
        grid (list[list[int]]): The 2D grid representing the terrain.
        blocks_before_turn (int): The number of blocks that can be moved in the same direction before turning.
        max_in_direction (int): The maximum number of consecutive blocks that can be moved in the same direction.

    Returns:
        int: The minimum heat loss incurred to reach the bottom-right corner of the grid.
    """
    memo = defaultdict(lambda: defaultdict(lambda: sys.maxsize))
    for direction in Direction:
        memo[(0, 0)][direction] = 0

    # Initialize the priority queue with the starting positions
    pq = []
    heapq.heappush(pq, (0, (0, 0), Direction.RIGHT.name))
    heapq.heappush(pq, (0, (0, 0), Direction.DOWN.name))

    while pq:
        heat_loss, position, dir_name = heapq.heappop(pq)
        direction = Direction[dir_name]
        if heat_loss > memo[position][direction]:
            continue
        x, y = position
        for block in range(max_in_direction):
            dx, dy = direction.value
            x, y = x + dx, y + dy
            if x < 0 or x >= len(grid[0]) or y < 0 or y >= len(grid):
                break
            heat_loss += grid[y][x]
            if block < blocks_before_turn:
                continue
            for new_dir in ALLOWED_CRUCIBLE_TURNS[direction]:
                if heat_loss < memo[(x, y)][new_dir]:
                    memo[(x, y)][new_dir] = heat_loss
                    heapq.heappush(pq, (heat_loss, (x, y), new_dir.name))

    return min(memo[(len(grid[0]) - 1, len(grid) - 1)].values())


if __name__ == "__main__":
    input_data = get_input("inputs/17_input.txt")

    print(f"Part 1: {compute(input_data, 0, 3)}")
    print(f"Part 2: {compute(input_data, 3, 10)}")
