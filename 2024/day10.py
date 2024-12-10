# pylint: disable=line-too-long
"""
Part 1: What is the sum of scores of all starting points, the score is the amount of times a starting point can reach a unique endpoint
Answer: 796

Part 2: What is the sum of the ratings of all trailheads, the rating is the amount of times a starting point can reach an endpoint
Answer: 1942
"""

from utils import profiler


def get_input(file_path: str) -> tuple[list, list]:
    """Get the input data"""
    grid = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            grid.append(list(map(int, line.strip())))

    # Every 0 is a starting point
    starting_points = [(x,y) for y, line in enumerate(grid) for x, c in enumerate(line) if c == 0]

    return grid, starting_points


def within_grid(x: int, y: int, x_limit: int, y_limit: int) -> bool:
    """Check whether we still are in the grid"""
    return 0 <= x < x_limit and 0 <= y < y_limit


def follow_path(grid: list, x: int, y: int, previous: tuple[int, int], path_ends: list) -> None:
    """Recursively walk through the grid, stop when we've reached the highest point"""
    if not within_grid(x, y, len(grid[0]), len(grid)):
        return

    current = grid[y][x]
    if current - previous != 1:
        return
    if current == 9:
        path_ends.append((x, y))
        return
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        follow_path(grid, x + dx, y + dy, current, path_ends)


@profiler
def part_one(grid: list, start_points: list) -> int:
    """Find how many endpoints we can reach for each starting point"""
    score_unique = []
    for x, y in start_points:
        path_ends = []
        follow_path(grid, x, y, -1, path_ends)
        score_unique.append(len(set(path_ends)))

    return sum(score_unique)


@profiler
def part_two(grid: list, start_points: list) -> int:
    """Find how many routes to an endpoint we can reach for each starting point"""
    score_rating = []
    for x, y in start_points:
        path_ends = []
        follow_path(grid, x, y, -1, path_ends)
        score_rating.append(len(path_ends))

    return sum(score_rating)


if __name__ == "__main__":
    # Get input data
    input_data, trailheads = get_input("inputs/10_input.txt")

    # Get solutions
    print(f"Part 1 = {part_one(input_data, trailheads)}")
    print(f"Part 2 = {part_two(input_data, trailheads)}")
