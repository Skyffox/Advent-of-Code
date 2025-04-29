# pylint: disable=line-too-long
"""
Part 1: How many trees are visible from outside the grid?
Answer: 1533

Part 2: What is the highest scenic score possible for any tree?
Answer: 345744
"""

from utils import profiler


def get_input(file_path: str) -> list:
    """Get the input data"""
    with open(file_path, "r", encoding="utf-8") as file:
        return [list(line.strip()) for line in file]


@profiler
def part_1(forrest: list) -> int:
    """
    Check for every position in the grid (a tree) whether all of the other trees between it and an edge of the grid are shorter than it. 
    Then it is visible. This only has to be true for one side not all of them.
    """
    visible_trees = len(forrest) * 2 + len(forrest[0]) * 2 - 4
    # Part 1
    for y in range(1, len(forrest) - 1):
        for x in range(1, len(forrest) - 1):
            # Left
            if all(forrest[y][x] > forrest[y][a] for a in range(x)):
                visible_trees += 1
                continue

            # Right
            if all(forrest[y][x] > forrest[y][a] for a in range(x + 1, len(forrest[0]))):
                visible_trees += 1
                continue

            # Top
            if all(forrest[y][x] > forrest[a][x] for a in range(y)):
                visible_trees += 1
                continue

            # Bottom
            if all(forrest[y][x] > forrest[a][x] for a in range(y + 1, len(forrest))):
                visible_trees += 1
                continue

    return visible_trees


@profiler
def part_2(forrest: list) -> int:
    """The elves want to build a treehouse and we need to calculate from what position we can see the most trees"""
    scenic_score = 0
    for y in range(1, len(forrest) - 1):
        for x in range(1, len(forrest) - 1):
            # Left
            score_left = 0
            for a in range(x-1, -1, -1):
                score_left += 1
                if forrest[y][x] <= forrest[y][a]:
                    break

            # Right
            score_right = 0
            for a in range(x+1, len(forrest[0])):
                score_right += 1
                if forrest[y][x] <= forrest[y][a]:
                    break

            # Top
            score_top = 0
            for a in range(y-1, -1, -1):
                score_top += 1
                if forrest[y][x] <= forrest[a][x]:
                    break

            # Bottom
            score_bottom = 0
            for a in range(y+1, len(forrest)):
                score_bottom += 1
                if forrest[y][x] <= forrest[a][x]:
                    break

            scenic_score = max(scenic_score, score_left * score_right * score_top * score_bottom)

    return scenic_score


if __name__ == "__main__":
    input_data = get_input("inputs/8_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
