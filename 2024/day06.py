# pylint: disable=line-too-long
"""
Part 1: Find out how many distinct tiles the guard visits
Answer: 5030

Part 2: If we could place an obstacle in any position in the grid how many times would we cause an infinite loop
Answer: 1928 (takes ~56 seconds)
"""

from copy import deepcopy
from utils import profiler


def within_grid(x: int, y: int, x_limit: int, y_limit: int) -> bool:
    """Check whether we still are in the grid"""
    return 0 <= x < x_limit and 0 <= y < y_limit


def patrol(grid: list, pos: tuple[int, int]) -> tuple[bool, list]:
    """
    Apply the rules on how the guard moves through the grid. We always go forward until we hit an object
    then we turn right and continue onward
    """
    # All possible direction we can move: N, E, S, W
    directions = ((0, -1), (1, 0), (0, 1), (-1, 0))
    idx = 0
    x_limit = len(grid[0])
    y_limit = len(grid)

    # A dictionary that saves the positions we have been, and which direction we faced when we entered the position
    visited = {pos: [idx]}

    while True:
        # Step to the next position
        next_pos = (pos[0] + directions[idx][0], pos[1] + directions[idx][1])

        # We have left the grid, also return the keys to show which tiles we have visited
        if not within_grid(next_pos[0], next_pos[1], x_limit, y_limit):
            return True, list(visited.keys())

        # Turn right based on the directions variable
        if grid[next_pos[1]][next_pos[0]] == "#":
            idx = (idx + 1) % 4
        else:
            # Check if we visited the position before and if we were in the same direction
            # that means we have entered a loop. Otherwise add the direction to the tile in our dictionary
            if next_pos in visited:
                if idx in visited[next_pos]:
                    return False, None
                visited.update({next_pos: visited[next_pos] + [idx]})
            else:
                visited[next_pos] = [idx]

            pos = next_pos


def get_input(file_path: str) -> tuple[list, tuple[int, int]]:
    """Get the input data"""
    grid = []
    start_pos = (0, 0)
    with open(file_path, "r", encoding="utf-8") as file:
        for idx, line in enumerate(file):
            grid.append(list(line.strip()))
            if "^" in line:
                start_pos = (line.index("^"), idx)

    return grid, start_pos


@profiler
def part_1(grid: list, start_pos: tuple[int, int]):
    """Get the tiles the guard visited"""
    _, visited = patrol(grid, start_pos)
    return len(visited)


@profiler
def part_2(grid: list, start_pos: tuple[int, int]) -> int:
    """Count how many times we can enter a loop if we place an object in the grid"""
    loops_count = 0
    # Get all the tiles the guard visited
    _, visited = patrol(grid, start_pos)

    # Do not count the position the guard starts
    visited.remove(start_pos)
    # We don't have to test every empty space, just the visited ones
    # because the obstruction must be on the visited path
    for x, y in visited:
        grid_cpy = deepcopy(grid)
        # Add an obstacle
        grid_cpy[y][x] = "#"

        has_left, _ = patrol(grid_cpy, start_pos)
        # Means we ended up in a loop
        if not has_left:
            loops_count += 1

    return loops_count


if __name__ == "__main__":
    # Get input data
    input_data, start = get_input("inputs/6_input.txt")

    print(f"Part 1: {part_1(input_data, start)}")
    print(f"Part 2: {part_2(input_data, start)}")
