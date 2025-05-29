# pylint: disable=line-too-long
"""
Day 17: Set and Forget

Part 1: Run your ASCII program. What is the sum of the alignment parameters for the scaffold intersections?
Answer: 3660

Part 2: After visiting every part of the scaffold at least once, how much dust does the vacuum robot report it has collected?
Answer: 962913
"""

from typing import List, Tuple
from utils import IntcodeComputer
from utils import profiler

MAX_REGISTER_LENGTH = 20
DIRS = {
    '^': (0, -1),
    'v': (0, 1),
    '<': (-1, 0),
    '>': (1, 0)
}


def get_input(file_path: str) -> List[int]:
    """
    Reads the input file and returns the Intcode program as a list of integers.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        List[int]: The Intcode program.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return list(map(int, file.read().strip().split(",")))


def build_map(program: List[int]) -> List[str]:
    """
    Runs the Intcode program to build the scaffold map.

    Args:
        program (List[int]): Intcode program.

    Returns:
        List[List[str]]: 2D map of scaffold (#) and open space (.) characters.
    """
    computer = IntcodeComputer(program)
    grid_output = []
    while not computer.halted:
        output = computer.run()
        if output is not None:
            grid_output.append(chr(output))
    return ''.join(grid_output).splitlines()


def find_intersections(grid: List[str]) -> List[Tuple[int, int]]:
    """
    Finds intersections where scaffolds (#) are surrounded up/down/left/right by scaffolds.

    Args:
        scaffold_map (List[List[str]]): 2D map.

    Returns:
        List[Tuple[int, int]]: Coordinates of intersections.
    """
    intersections = []
    for y in range(1, len(grid) - 1):
        for x in range(1, len(grid[y]) - 1):
            if grid[y][x] == '#' and all(grid[y + dy][x + dx] == '#' for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]):
                intersections.append((x, y))
    return intersections


@profiler
def part_one(data_input: List[int]) -> int:
    """
    Calculates the sum of alignment parameters of the scaffold intersections.

    Args:
        data_input (List[int]): Intcode program.

    Returns:
        int: Sum of alignment parameters (x * y).
    """
    scaffold_map = build_map(data_input)
    intersections = find_intersections(scaffold_map)
    return sum(x * y for x, y in intersections)


def turn_left(dx, dy):
    """Returns a left-turned direction vector."""
    return (dy, -dx)


def turn_right(dx, dy):
    """Returns a right-turned direction vector."""
    return (-dy, dx)


def add_pos(pos, delta):
    """Adds a movement vector to a position."""
    return (pos[0] + delta[0], pos[1] + delta[1])


def find_path(scaffold: set, start_pos: Tuple[int, int], start_dir: Tuple[int, int]) -> List[str]:
    """
    Determines the movement path as a sequence of 'L', 'R', and step counts.

    Args:
        scaffold (set): Set of (x, y) positions representing the scaffold.
        start_pos (Tuple[int, int]): Starting position of the robot.
        start_dir (Tuple[int, int]): Starting direction vector.

    Returns:
        List[str]: Movement path in turn and step instructions.
    """
    pos = start_pos
    dir = start_dir
    path = []

    def can_move(p, d):
        return add_pos(p, d) in scaffold

    while True:
        steps = 0
        # Move forward while possible
        while can_move(pos, dir):
            pos = add_pos(pos, dir)
            steps += 1
        if steps > 0:
            path.append(str(steps))

        # Try turn left
        left_dir = turn_left(*dir)
        if can_move(pos, left_dir):
            path.append('L')
            dir = left_dir
            continue

        # Try turn right
        right_dir = turn_right(*dir)
        if can_move(pos, right_dir):
            path.append('R')
            dir = right_dir
            continue

        # Can't move or turn - done
        break

    return path


def find_start_and_dir(map_lines: List[str]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """
    Locates the robot's starting position and facing direction.

    Args:
        map_lines (List[str]): The scaffold map.

    Returns:
        Tuple[Tuple[int, int], Tuple[int, int]]: Starting position and direction vector.
    """
    for y, line in enumerate(map_lines):
        for x, char in enumerate(line):
            if char in ['^', 'v', '<', '>']:
                return (x, y), DIRS[char]
    raise ValueError("No robot start position found")


def find_repeat(path: List[str], registers=[], sequence=[]) -> Tuple[bool, List[List[str]], List[int]]:
    """
    Recursively finds up to 3 repeating path subsequences that fit in 20-char limits.

    Args:
        path (List[str]): Full path of robot instructions.
        registers (List[List[str]]): Current candidate functions.
        sequence (List[int]): Sequence of register indices used.

    Returns:
        Tuple[bool, List[List[str]], List[int]]: Whether a match was found, functions, and main sequence.
    """
    cleared = False
    while not cleared:
        cleared = True

        for i, prev in enumerate(registers):
            if len(prev) <= len(path) and path[:len(prev)] == prev:
                path = path[len(prev):]
                sequence.append(i)
                cleared = False
                break

    if len(registers) == 3:
        return (True, registers, sequence) if len(path) == 0 else (False, None, None)

    register_len = min(len(path), MAX_REGISTER_LENGTH // 2)

    # Our string form of the path must fit within our register constraint
    # we start on a turn, so we do not want to end on a turn
    # repeats could then be (turn, turn, #), which is not an efficient sequence
    while len(",".join(path[:register_len])) > MAX_REGISTER_LENGTH or path[register_len - 1] in {'R', 'L'}:
        register_len -= 1

    while register_len > 0:
        res, matches, seq = find_repeat(path, registers + [path[:register_len]], sequence.copy())
        if res:
            return res, matches, seq
        register_len -= 2

    return False, [], []


def drive_bot(codes: List[int], main: str, registers: List[str]) -> int:
    """
    Runs the robot program with movement functions and returns the dust collected.

    Args:
        codes (List[int]): Intcode program.
        main (str): Main routine using 'A', 'B', 'C'.
        registers (List[str]): Movement subroutines A, B, and C.

    Returns:
        int: Dust collected.
    """
    computer = IntcodeComputer(codes)
    computer.memory[0] = 2 # Set address 0 to 2 as required

    # Prepare all inputs as ASCII codes + newlines
    inputs = (
        [ord(c) for c in main] + [ord('\n')] +
        [ord(c) for c in registers[0]] + [ord('\n')] +
        [ord(c) for c in registers[1]] + [ord('\n')] +
        [ord(c) for c in registers[2]] + [ord('\n')] +
        [ord('n'), ord('\n')]  # video feed: no
    )
    # Feed inputs into computer input buffer
    for i in inputs:
        computer.add_input(i)

    last_output = None
    while not computer.halted:
        output = computer.run()
        if output is not None:
            last_output = output

    return last_output


@profiler
def part_two(program: List[int]) -> int:
    """
    Runs the robot vacuum program with movement routines to collect dust.

    Args:
        data_input (List[int]): Intcode program.

    Returns:
        int: Amount of dust collected.
    """
    scaffold_map = build_map(program)
    scaffold_coords = {(x, y) for y, line in enumerate(scaffold_map) for x, char in enumerate(line) if char == '#'}

    path = find_path(scaffold_coords, *find_start_and_dir(scaffold_map))
    _, registers, sequence = find_repeat(path)
    main = ",".join(chr(x + ord('A')) for x in sequence)
    regcode = [",".join(x) for x in registers]

    return drive_bot(program, main, regcode)


if __name__ == "__main__":
    input_data = get_input("inputs/17_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
