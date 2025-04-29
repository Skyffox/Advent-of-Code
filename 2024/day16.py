# pylint: disable=line-too-long
"""
Part 1: Analyze your map carefully. What is the lowest score a Reindeer could possibly get?
Answer: 88468

Part 2: Analyze your map further. How many tiles are part of at least one of the best paths through the maze?
Answer: 616
"""

from heapq import heappop, heappush
from utils import profiler


def get_input(file_path: str) -> list:
    """Get the input data"""
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
def part_1(grid: list, start: tuple[int, int], end: tuple[int, int]) -> int:
    """Find the route that would get the lowest score to reach the end"""
    grid[end[0]] = grid[end[0]].replace('E', '.')
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    heap = [(0, 0, *start)]
    visited = set()
    while heap:
        score, d, i, j = heappop(heap)
        if (i, j) == end:
            break

        if (d, i, j) in visited:
            continue

        visited.add((d, i, j))

        x = i + directions[d][0]
        y = j + directions[d][1]
        if grid[x][y] == '.' and (d, x, y) not in visited:
            heappush(heap, (score + 1, d, x, y))

        left = (d - 1) % 4
        if (left, i, j) not in visited:
            heappush(heap, (score + 1000, left, i, j))

        right = (d + 1) % 4
        if (right, i, j) not in visited:
            heappush(heap, (score + 1000, right, i, j))

    return score


@profiler
def part_2(grid: list, start: tuple[int, int], end: tuple[int, int]) -> int:
    """Get all routes that have the lowest scores"""
    grid[end[0]] = grid[end[0]].replace('E', '.')

    def can_visit(d, i, j, score):
        prev_score = visited.get((d, i, j))
        if prev_score and prev_score < score:
            return False
        visited[(d, i, j)] = score
        return True

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    heap = [(0, 0, *start, {start})]
    visited = {}
    lowest_score = None
    winning_paths = set()
    while heap:
        score, d, i, j, path = heappop(heap)
        if lowest_score and lowest_score < score:
            break

        if (i, j) == end:
            lowest_score = score
            winning_paths |= path
            continue

        if not can_visit(d, i, j, score):
            continue

        x = i + directions[d][0]
        y = j + directions[d][1]
        if grid[x][y] == '.' and can_visit(d, x, y, score+1):
            heappush(heap, (score + 1, d, x, y, path | {(x, y)}))

        left = (d - 1) % 4
        if can_visit(left, i, j, score + 1000):
            heappush(heap, (score + 1000, left, i, j, path))

        right = (d + 1) % 4
        if can_visit(right, i, j, score + 1000):
            heappush(heap, (score + 1000, right, i, j, path))

    return len(winning_paths)


if __name__ == "__main__":
    # Get input data
    input_data, start_data, end_data = get_input("inputs/16_input.txt")

    print(f"Part 1: {part_1(input_data, start_data, end_data)}")
    print(f"Part 2: {part_2(input_data, start_data, end_data)}")
