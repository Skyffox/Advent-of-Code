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
    Parses the maze grid from the input file and locates start and end positions.

    Args:
        file_path (str): Path to the maze input file.

    Returns:
        Tuple containing:
            - grid (List[str]): Maze rows as strings.
            - start (Tuple[int, int]): Coordinates (row, col) of the start position marked 'S'.
            - end (Tuple[int, int]): Coordinates (row, col) of the end position marked 'E'.
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
    Computes the minimum score path from start to end in the maze.

    Scoring rules:
        - Moving forward one tile costs 1 point.
        - Turning left or right costs 1000 points.
    
    Uses a modified Dijkstra's algorithm that keeps track of direction to
    correctly accumulate turn costs.

    Args:
        grid (List[str]): Maze grid.
        start (Tuple[int, int]): Start coordinates.
        end (Tuple[int, int]): End coordinates.

    Returns:
        int: The minimum score required to reach the end.
    """
    # Replace 'E' with '.' to allow traversal
    grid[end[0]] = grid[end[0]].replace('E', '.')

    # Directions encoded as: 0=right, 1=down, 2=left, 3=up
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # Heap entries: (score, direction, row, col)
    heap = [(0, 0, *start)]
    visited = set()

    while heap:
        score, d, i, j = heappop(heap)

        # Stop if reached end
        if (i, j) == end:
            return score

        if (d, i, j) in visited:
            continue
        visited.add((d, i, j))

        # Attempt to move forward in current direction
        x, y = i + directions[d][0], j + directions[d][1]
        if grid[x][y] == '.' and (d, x, y) not in visited:
            heappush(heap, (score + 1, d, x, y))

        # Turn left (adds 1000 to score)
        left = (d - 1) % 4
        if (left, i, j) not in visited:
            heappush(heap, (score + 1000, left, i, j))

        # Turn right (adds 1000 to score)
        right = (d + 1) % 4
        if (right, i, j) not in visited:
            heappush(heap, (score + 1000, right, i, j))


@profiler
def part_2(grid: List[str], start: Tuple[int, int], end: Tuple[int, int]) -> int:
    """
    Determines how many unique tiles lie on at least one optimal (lowest-score) path.

    This function explores all optimal paths by:
        - Tracking path sets in the heap.
        - Keeping only paths with scores <= the best known score.
        - Collecting all tiles visited in any of these best paths.

    Args:
        grid (List[str]): Maze grid.
        start (Tuple[int, int]): Start coordinates.
        end (Tuple[int, int]): End coordinates.

    Returns:
        int: Count of unique tiles that appear on any lowest-cost path.
    """
    # Replace 'E' with '.' to allow traversal
    grid[end[0]] = grid[end[0]].replace('E', '.')

    # Memoization to avoid processing states with worse scores
    visited = {}

    def can_visit(d: int, i: int, j: int, score: int) -> bool:
        """
        Check if the current state (direction and position) can be visited
        with a better or equal score.

        Args:
            d (int): Current direction.
            i (int): Row coordinate.
            j (int): Column coordinate.
            score (int): Current path score.

        Returns:
            bool: True if this state is either not visited or can be visited with
                  a better (lower or equal) score.
        """
        prev_score = visited.get((d, i, j))
        if prev_score is not None and prev_score < score:
            return False
        visited[(d, i, j)] = score
        return True

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # Heap entries: (score, direction, row, col, path_set)
    heap = [(0, 0, *start, {start})]
    lowest_score = None
    winning_paths_tiles = set()

    while heap:
        score, d, i, j, path = heappop(heap)

        # If we have found a better solution, discard worse paths
        if lowest_score is not None and score > lowest_score:
            break

        # Reached end - update lowest_score and accumulate path tiles
        if (i, j) == end:
            lowest_score = score
            winning_paths_tiles |= path
            continue

        if not can_visit(d, i, j, score):
            continue

        # Move forward
        x, y = i + directions[d][0], j + directions[d][1]
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

    return len(winning_paths_tiles)


if __name__ == "__main__":
    input_data, start_data, end_data = get_input("inputs/16_input.txt")

    print(f"Part 1: {part_1(input_data, start_data, end_data)}")
    print(f"Part 2: {part_2(input_data, start_data, end_data)}")
