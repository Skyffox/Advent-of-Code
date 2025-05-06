# pylint: disable=line-too-long
"""
Day 10: Pipe Maze

Part 1: How many steps along the loop does it take to get from the starting position to the point farthest from the starting position?
Answer: 6757

Part 2: How many tiles are enclosed by the loop?
Answer: 523
"""

from utils import profiler


def get_input(file_path: str) -> tuple:
    """
    Reads the input file and extracts the grid of pipes and the starting position.

    The input file consists of a grid of characters, where each character represents a part of the loop, 
    and the starting position is marked by 'S'.

    Args:
        file_path (str): The path to the input file containing the grid.

    Returns:
        tuple: A tuple containing two elements:
            - A list of lists representing the grid of pipes.
            - A tuple (r, c) representing the row and column indices of the starting position.
    """
    lst = []
    starting_pos = (0, 0)
    with open(file_path, "r", encoding="utf-8") as file:
        for i, line in enumerate(file):
            line = list(line.strip())
            lst.append(line)
            if 'S' in line:
                starting_pos = (i, line.index("S"))

    return lst, starting_pos


@profiler
def part_1(grid, start_r, start_c):
    """
    Determines how many steps it takes to get from the starting position to the point 
    farthest from the starting position along the loop.

    The loop consists of pipes that define the directions to take. This function simulates the movement 
    along the loop starting from the initial position and stops once it completes the loop. It counts 
    the number of steps taken to reach the farthest point from the starting position.

    Args:
        grid (list): The grid of pipes representing the loop.
        start_r (int): The row index of the starting position.
        start_c (int): The column index of the starting position.

    Returns:
        tuple: A tuple containing:
            - A set of coordinates that represent the positions visited during the loop.
            - The total number of steps taken to complete the loop.
    """
    directions = ((-1, 0), (1, 0), (0, -1), (0, 1))
    possible_pipes = ('|F7', '|LJ', '-FL', '-J7')
    steps = 0

    # Find the starting direction based on adjacent pipes
    for (delta_r, delta_c), pipes in zip(directions, possible_pipes):
        r, c = start_r + delta_r, start_c + delta_c
        if grid[r][c] in pipes:
            dr, dc = delta_r, delta_c
            r, c = start_r, start_c
            break

    seen = set([(r, c)])
    # Take steps and track the direction
    while True:
        r, c = r + dr, c + dc
        pipe = grid[r][c]
        seen.add((r, c))
        steps += 1

        # Update direction based on the pipe type
        if pipe in 'L7':
            dr, dc = dc, dr
        elif pipe in 'FJ':
            dr, dc = -dc, -dr
        elif pipe == 'S':
            break

    return seen, steps


@profiler
def part_2(grid, main_loop):
    """
    Calculates the number of tiles enclosed by the loop found in Part 1.

    This function iterates over the grid and determines the area enclosed by the loop by tracking 
    the boundaries defined by the pipes. The loop's enclosure is determined by checking whether 
    a cell is inside the loop and counting the enclosed area.

    Args:
        grid (list): The grid of pipes representing the loop.
        main_loop (set): A set of coordinates representing the positions that form the loop.

    Returns:
        int: The total number of tiles enclosed by the loop.
    """
    area = 0

    for r, row in enumerate(grid):
        inside = False
        for c, cell in enumerate(row):
            if (r, c) not in main_loop:
                area += inside
            else:
                inside = inside ^ (cell in '|F7')

    return area


if __name__ == "__main__":
    input_data, start = get_input("inputs/10_input.txt")

    loop, loop_len = part_1(input_data, *start)

    print(f"Part 1: {loop_len // 2}")
    print(f"Part 2: {part_2(input_data, loop)}")
