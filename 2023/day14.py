# pylint: disable=line-too-long
"""
Day 14: Parabolic Reflector Dish

Part 1: After tilting the platform north once, compute the total load on the support beams.
Answer: 110407

Part 2: After 1 billion full spin cycles (tilting N, W, S, E), compute the total load.
Answer: 87273
"""

from typing import List, Set, Tuple
from utils import profiler

Position = Tuple[int, int]


def get_input(file_path: str) -> List[str]:
    """
    Reads the puzzle input from a file.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        List[str]: List of strings representing the puzzle grid.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file]


def parse(data: List[str]) -> Tuple[Set[Position], Set[Position], int, int]:
    """
    Parses the input grid into sets of round and cube rock positions.

    Args:
        data (List[str]): Grid represented as a list of strings.

    Returns:
        Tuple:
            - Set[Position]: Coordinates of round rocks ('O').
            - Set[Position]: Coordinates of cube rocks ('#').
            - int: Number of columns.
            - int: Number of rows.
    """
    round_rocks = set()
    cube_rocks = set()
    for y, row in enumerate(data):
        for x, ch in enumerate(row):
            if ch == 'O':
                round_rocks.add((x, y))
            elif ch == '#':
                cube_rocks.add((x, y))
    return round_rocks, cube_rocks, len(data[0]), len(data)


def tilt(rounds: Set[Position], cubes: Set[Position], cols: int, rows: int) -> Set[Position]:
    """
    Simulates tilting the platform northward, causing round rocks to slide up until blocked.

    Args:
        rounds (Set[Position]): Positions of round rocks.
        cubes (Set[Position]): Positions of cube rocks (obstacles).
        cols (int): Width of the grid.
        rows (int): Height of the grid.

    Returns:
        Set[Position]: Updated positions of round rocks after tilting.
    """
    new_rounds = set()
    for x in range(cols):
        stop = 0
        for y in range(rows):
            pos = (x, y)
            if pos in cubes:
                stop = y + 1
            elif pos in rounds:
                new_rounds.add((x, stop))
                stop += 1
    return new_rounds


def rotate_clockwise(points: Set[Position], cols: int) -> Set[Position]:
    """
    Rotates a set of coordinates 90 degrees clockwise.

    Args:
        points (Set[Position]): Coordinates to rotate.
        cols (int): Width of the grid (used to determine rotation).

    Returns:
        Set[Position]: Rotated coordinates.
    """
    return {(cols - y - 1, x) for x, y in points}


def get_load(rounds: Set[Position], rows: int) -> int:
    """
    Calculates the total load on the north support beams.
    The load of each rock is proportional to how far it is from the north edge.

    Args:
        rounds (Set[Position]): Coordinates of round rocks.
        rows (int): Height of the grid.

    Returns:
        int: Total load value.
    """
    return sum(rows - y for _, y in rounds)


@profiler
def part_one(data: List[str]) -> int:
    """
    Solves Part 1: compute the load after tilting north once.

    Args:
        data (List[str]): The input puzzle grid.

    Returns:
        int: Total load on the support beams.
    """
    rounds, cubes, cols, rows = parse(data)
    rounds = tilt(rounds, cubes, cols, rows)
    return get_load(rounds, rows)


@profiler
def part_two(data: List[str]) -> int:
    """
    Solves Part 2: simulates 1 billion spin cycles with cycle detection.

    Each cycle consists of four tilt-rotate operations (N → W → S → E).
    Once a repeating state is found, fast-forwards to the final state.

    Args:
        data (List[str]): The input puzzle grid.

    Returns:
        int: Total load on the support beams after all cycles.
    """
    rounds, cubes, cols, rows = parse(data)
    seen = {}
    history = []

    for cycle in range(1_000_000_000):
        state = frozenset(rounds)
        if state in seen:
            loop_start = seen[state]
            loop_len = cycle - loop_start
            remaining = (1_000_000_000 - loop_start) % loop_len
            return history[loop_start + remaining]
        seen[state] = cycle
        history.append(get_load(rounds, rows))

        for _ in range(4):
            rounds = tilt(rounds, cubes, cols, rows)
            rounds = rotate_clockwise(rounds, cols)
            cubes = rotate_clockwise(cubes, cols)

    return get_load(rounds, rows)


if __name__ == "__main__":
    input_data = get_input("inputs/14_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
