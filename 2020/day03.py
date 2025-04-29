# pylint: disable=line-too-long
"""
Part 1: Find all the trees we encounter if go down 1 and 3 to the right for each step
Answer: 278

Part 2: Do the same but for different steps to the right and bottom
Answer: 9709761600
"""

from utils import profiler


def get_input(file_path: str) -> list:
    """Get the input data"""
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file]


def slope(grid: list, dx: int, dy: int) -> int:
    """We go down a slope with dx for x and dy for y at each step and count into how many trees we crash"""
    n, x, y = 0, 0, 0
    while y < len(grid) - 1:
        x += dx
        y += dy

        # We can't keep propagating to the right, so we need to "reset" the grid
        if x >= len(grid[0]):
            x %= len(grid[0])

        # Tree encountered
        if grid[y][x] == "#":
            n += 1

    return n


@profiler
def part_1(grid: list) -> int:
    """Count the number of trees encountered when we move 3 steps to the right and 1 down at each iteration"""
    return slope(grid, 3, 1)


@profiler
def part_2(grid: list) -> int:
    """Multiply together the number of trees encountered on each of the slopes below"""
    n = 1
    n *= slope(grid, 1, 1)
    n *= slope(grid, 3, 1)
    n *= slope(grid, 5, 1)
    n *= slope(grid, 7, 1)
    n *= slope(grid, 1, 2)

    return n


if __name__ == "__main__":
    input_data = get_input("inputs/3_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
