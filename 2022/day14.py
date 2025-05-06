# pylint: disable=line-too-long
"""
Day 14: Regolith Reservoir

Part 1: How many units of sand come to rest before sand starts flowing into the abyss below?
Answer: 728

Part 2: Using your scan, simulate the falling sand until the source of the sand becomes blocked. How many units of sand come to rest?
Answer: 27623
"""

from typing import List, Tuple
from utils import profiler


def get_input(file_path: str) -> List[List[int]]:
    """
    Parse the input file to extract the wall coordinates.

    The input consists of coordinates describing the walls of the terrain.
    For each pair of coordinates, a line is drawn between them, and the terrain is marked by '#' where walls exist.
    
    Args:
        file_path (str): Path to the input file.

    Returns:
        List[List[int]]: A list of wall coordinates where each element is a pair of x and y coordinates.
    """
    walls = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip().split(" -> ")
            line = [list(map(int, x.split(","))) for x in line]

            for idx, (x, y) in enumerate(line):
                walls.append([x, y])
                if idx == len(line) - 1:
                    break

                # Find all the walls, input is as follows: 498,4 -> 498,6 -> 496,6
                # A line is drawn between these points, that is where the walls are
                next_point = line[idx + 1]
                diff = abs(x - next_point[0]) if x != next_point[0] else abs(y - next_point[1])
                for d in range(1, diff):
                    # Check whether the difference is between the x or y coordinate
                    if x != next_point[0]:
                        # Check whether the line goes left or right
                        walls.append([x + (d if x < next_point[0] else -d), y])
                    else:
                        walls.append([x, y + (d if y < next_point[1] else -d)])

    return walls


def draw_canvas(walls: List[List[int]], min_x: int, max_x: int, max_y: int) -> List[List[str]]:
    """
    Creates a visual representation of the terrain with walls and sand source.

    Args:
        walls (List[List[int]]): The list of wall coordinates.
        min_x (int): The minimum x-coordinate of the grid.
        max_x (int): The maximum x-coordinate of the grid.
        max_y (int): The maximum y-coordinate of the grid.

    Returns:
        List[List[str]]: A 2D grid where walls are represented as '#', air as '.', and the sand source as '+'.
    """
    canvas = []
    for y in range(max_y + 1):
        canvas_line = []
        for pos_x in range(min_x, max_x + 1):
            if [pos_x, y] in walls:
                canvas_line.append("# ")
            elif [pos_x, y] == [500, 0]:
                canvas_line.append("+ ")
            else:
                canvas_line.append(". ")
        canvas.append(canvas_line)

    return canvas


def sand_propagation(canvas: List[List[str]], sand_start: Tuple[int, int], min_x: int) -> bool:
    """
    Simulates the movement of a sand particle from the source to the rest position.

    The sand can fall straight down or diagonally left or right depending on the availability of empty space.
    If the sand reaches the abyss or falls off the grid, the function returns `True` indicating the sand has fallen off.
    If the sand comes to rest, the function returns `False`.

    Args:
        canvas (List[List[str]]): The visual grid representing the terrain.
        sand_start (Tuple[int, int]): The starting position of the sand source.
        min_x (int): The minimum x-coordinate for the grid.

    Returns:
        bool: `True` if the sand flows into the abyss, `False` if it comes to rest.
    """
    y = sand_start[1]
    x = sand_start[0] - min_x

    while True:
        if y > len(canvas) - 2 or x < 0 or x > len(canvas[0]) - 1:
            return True

        if canvas[y + 1][x] == ". ":
            y += 1
        elif canvas[y + 1][x - 1] == ". ":
            x -= 1
            y += 1
        elif canvas[y + 1][x + 1] == ". ":
            x += 1
            y += 1
        else:
            if canvas[y][x] == "+ ":
                return True

            canvas[y][x] = "* "
            return False


@profiler
def part_1(walls: List[List[int]]) -> int:
    """
    Simulates sand falling into the grid until it overflows or comes to rest.
    In this part, the goal is to count how many units of sand come to rest before it starts flowing into the abyss.
    
    Args:
        walls (List[List[int]]): A list of wall coordinates.

    Returns:
        int: The number of sand units that come to rest before the sand overflows into the abyss.
    """
    overflow_count = 0

    min_x = min([x[0] for x in walls])
    max_x = max([x[0] for x in walls])
    max_y = max([x[1] for x in walls])

    canvas = draw_canvas(walls, min_x, max_x, max_y)

    while True:
        overflow_count += 1
        if sand_propagation(canvas, (500, 0), min_x):
            return overflow_count - 1


@profiler
def part_2(walls: List[List[int]]) -> int:
    """
    Simulates sand falling until the sand source is blocked.
    In this part, the goal is to simulate the falling sand until the source becomes blocked, 
    and then count how many units of sand come to rest.

    Args:
        walls (List[List[int]]): A list of wall coordinates.

    Returns:
        int: The number of sand units that come to rest until the source becomes blocked.
    """
    overflow_count = 0

    min_x = min([x[0] for x in walls])
    max_x = max([x[0] for x in walls])
    max_y = max([x[1] for x in walls])

    min_x -= 200
    max_x += 200

    canvas = draw_canvas(walls, min_x, max_x, max_y)

    canvas.append([". " for _ in range(min_x, max_x + 1)])
    canvas.append(["# " for _ in range(min_x, max_x + 1)])

    while True:
        overflow_count += 1
        if sand_propagation(canvas, (500, 0), min_x):
            return overflow_count


if __name__ == "__main__":
    input_data = get_input("inputs/14_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
