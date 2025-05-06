# pylint: disable=line-too-long
"""
Day 16: Reindeer Maze

Part 1: Analyze your map carefully. What is the lowest score a Reindeer could possibly get?
Answer: 88468

Part 2: Analyze your map further. How many tiles are part of at least one of the best paths through the maze?
Answer: 616
"""

from heapq import heappop, heappush
from typing import List, Tuple
from utils import profiler


def get_input(file_path: str) -> Tuple[List[str], Tuple[int, int], Tuple[int, int]]:
    """
    Parse the maze input and extract the start and end positions.

    Returns:
        tuple[list[str], tuple[int, int], tuple[int, int]]: Grid lines, start (row, col), end (row, col).
    """
    grid = []
    start, end = (0, 0), (0, 0)
    with open(file_path, "r", encoding="utf-8") as file:
        for idx, line in enumerate(file):
            line = line.strip()
            if "S" in line:
                start = (idx, line.index("S"))
            if "E" in line:
                end = (idx, line.index("E"))
            grid.append(line)

    return grid, start, end


@profiler
def part_1(grid: List[str], start: Tuple[int, int], end: Tuple[int, int]) -> int:
    """
    Find the path with the lowest score from start to end in the maze.
    Moving straight costs 1. Turning left or right costs 1000.
    Uses Dijkstra's algorithm variant to track minimal path cost based on direction.

    Returns:
        int: Minimum score to reach the end.
    """
    grid[end[0]] = grid[end[0]].replace('E', '.')
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    heap = [(0, 0, *start)] # (score, direction, row, col)
    visited = set()

    while heap:
        score, d, i, j = heappop(heap)
        if (i, j) == end:
            break

        if (d, i, j) in visited:
            continue
        visited.add((d, i, j))

        # Forward movement
        x = i + directions[d][0]
        y = j + directions[d][1]
        if grid[x][y] == '.' and (d, x, y) not in visited:
            heappush(heap, (score + 1, d, x, y))

        # Turn left
        left = (d - 1) % 4
        if (left, i, j) not in visited:
            heappush(heap, (score + 1000, left, i, j))

        # Turn right
        right = (d + 1) % 4
        if (right, i, j) not in visited:
            heappush(heap, (score + 1000, right, i, j))

    return score


@profiler
def part_2(grid: List[str], start: Tuple[int, int], end: Tuple[int, int]) -> int:
    """
    Find how many tiles are on at least one path with the lowest score.
    Tracks all optimal paths and counts unique tiles that are part of any such path.

    Returns:
        int: Number of unique tiles involved in any best path.
    """
    grid[end[0]] = grid[end[0]].replace('E', '.')

    def can_visit(d: int, i: int, j: int, score: int) -> bool:
        prev_score = visited.get((d, i, j))
        if prev_score and prev_score < score:
            return False
        visited[(d, i, j)] = score
        return True

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    heap = [(0, 0, *start, {start})] # (score, dir, row, col, path_set)
    visited = {}
    lowest_score = None
    winning_paths = set()

    while heap:
        score, d, i, j, path = heappop(heap)

        if lowest_score and score > lowest_score:
            break

        if (i, j) == end:
            lowest_score = score
            winning_paths |= path
            continue

        if not can_visit(d, i, j, score):
            continue

        # Forward movement
        x = i + directions[d][0]
        y = j + directions[d][1]
        if grid[x][y] == '.' and can_visit(d, x, y, score + 1):
            heappush(heap, (score + 1, d, x, y, path | {(x, y)}))

        # Turn left
        left = (d - 1) % 4
        if can_visit(left, i, j, score + 1000):
            heappush(heap, (score + 1000, left, i, j, path))

        # Turn right
        right = (d + 1) % 4
        if can_visit(right, i, j, score + 1000):
            heappush(heap, (score + 1000, right, i, j, path))

    return len(winning_paths)


if __name__ == "__main__":
    input_data, start_data, end_data = get_input("inputs/16_input.txt")

    print(f"Part 1: {part_1(input_data, start_data, end_data)}")
    print(f"Part 2: {part_2(input_data, start_data, end_data)}")
