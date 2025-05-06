# pylint: disable=line-too-long
"""
Day 8: Treetop Tree House

Part 1: How many trees are visible from outside the grid?
Answer: 1533

Part 2: What is the highest scenic score possible for any tree?
Answer: 345744
"""

from utils import profiler


def get_input(file_path: str) -> list[list[int]]:
    """
    Reads the input file and converts it into a 2D list of integers representing tree heights.

    Each line in the input file corresponds to a row in the grid, and each character in a line 
    represents the height of a tree at that position.

    Args:
        file_path (str): The path to the input file containing the tree heights.

    Returns:
        list[list[int]]: A 2D list of integers where each element represents the height of a tree 
                         in the grid at that position.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [[int(ch) for ch in line.strip()] for line in file]


@profiler
def part_1(forest: list[list[int]]) -> int:
    """
    Determines how many trees are visible from the outside of the grid. A tree is considered visible 
    if there are no taller or equal-height trees between it and the edge of the grid in any of the 
    four directions (left, right, top, bottom).

    Args:
        forest (list[list[int]]): A 2D list representing the grid of trees, where each element is 
                                  the height of a tree.

    Returns:
        int: The number of trees that are visible from outside the grid.
    """
    height = len(forest)
    width = len(forest[0])
    visible = 0

    # Iterate through each tree in the grid
    for y in range(height):
        for x in range(width):
            current = forest[y][x]

            # Check if the tree is visible from any direction
            if (
                all(forest[y][a] < current for a in range(x)) or                        # left
                all(forest[y][a] < current for a in range(x + 1, width)) or             # right
                all(forest[a][x] < current for a in range(y)) or                        # top
                all(forest[a][x] < current for a in range(y + 1, height))               # bottom
            ):
                visible += 1

    return visible


@profiler
def part_2(forest: list[list[int]]) -> int:
    """
    Computes the highest scenic score possible for any tree in the grid. The scenic score of a tree 
    is calculated by multiplying the viewing distances in all four directions (left, right, up, down).
    The viewing distance in a direction is the number of trees that can be seen until a taller or equally 
    tall tree blocks the view.

    Args:
        forest (list[list[int]]): A 2D list representing the grid of trees, where each element is 
                                  the height of a tree.

    Returns:
        int: The highest scenic score among all trees in the grid.
    """
    height = len(forest)
    width = len(forest[0])
    best_score = 0

    # Iterate through each tree in the grid
    for y in range(height):
        for x in range(width):
            current = forest[y][x]

            # Calculate the viewing distances in all four directions
            left = right = up = down = 0

            # Check left viewing distance
            for dx in range(x - 1, -1, -1):
                left += 1
                if forest[y][dx] >= current:
                    break

            # Check right viewing distance
            for dx in range(x + 1, width):
                right += 1
                if forest[y][dx] >= current:
                    break

            # Check up viewing distance
            for dy in range(y - 1, -1, -1):
                up += 1
                if forest[dy][x] >= current:
                    break

            # Check down viewing distance
            for dy in range(y + 1, height):
                down += 1
                if forest[dy][x] >= current:
                    break

            # Calculate the scenic score and update the best score if it's higher
            score = left * right * up * down
            best_score = max(best_score, score)

    return best_score


if __name__ == "__main__":
    input_data = get_input("inputs/8_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
