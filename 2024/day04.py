# pylint: disable=line-too-long
"""
Part 1: Find the word XMAS in all possible directions in a grid
Answer: 2532

Part 2: Find an X of MAS in the same grid
Answer: 1941
"""

from utils import profiler


def search(grid: list, word: list, row: int, col: int, step_x: int, step_y: int) -> bool:
    """See if we can find a certain word when we step into a certain direction of the grid"""
    y_max = len(grid) - 1
    x_max = len(grid[0]) - 1
    for l in word:
        # See if we go out of bounds
        if row < 0 or row > x_max or col < 0 or col > y_max:
            return False
        # Checks whether we start at an X, or the starting letter of our word
        if l != grid[row][col]:
            return False

        row += step_x
        col += step_y

    return True


def get_input(file_path: str) -> list:
    """Get the input data"""
    with open(file_path, "r", encoding="utf-8") as file:
        return [list(line.strip()) for line in file]


@profiler
def part_1(grid: list) -> int:
    """Find the word XMAS in the grid like a word search puzzle"""
    occurences = 0
    directions = [-1, 0, 1]
    for col_idx, row in enumerate(grid):
        for row_idx, _ in enumerate(row):
            # Do a search for each direction to see if we can find a word
            for step_y in directions:
                for step_x in directions:
                    if step_x == step_y == 0:
                        continue

                    if search(grid, "XMAS", row_idx, col_idx, step_x, step_y):
                        occurences += 1

    return occurences


@profiler
def part_2(grid: list) -> int:
    """Find every X shaped MAS in our input"""
    occurences = 0
    for col_idx, row in enumerate(grid):
        for row_idx, _ in enumerate(row):
            # Check the topleft to bottomright diagonal for either MAS or SAM then do the same for the topright to bottomleft diagonal
            if (search(grid, "MAS", row_idx, col_idx, 1, 1) or search(grid, "SAM", row_idx, col_idx, 1, 1)) and \
               (search(grid, "MAS", row_idx + 2, col_idx, -1, 1) or search(grid, "SAM", row_idx + 2, col_idx, -1, 1)):
                occurences += 1

    return occurences


if __name__ == "__main__":
    # Get input data
    input_data = get_input("inputs/4_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
