# pylint: disable=line-too-long
"""
Day 11: Space Police

Part 1: Build a new emergency hull painting robot and run the Intcode program on it. How many panels does it paint at least once?
Answer: 2319

Part 2: After starting the robot on a single white panel instead, what registration identifier does it paint on your hull?
Answer: UERPRFGJ
"""

from typing import List, Tuple
from collections import defaultdict
from utils import IntcodeComputer
from utils import profiler


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


class Robot:
    """
    Represents a painting robot on a 2D grid.

    The robot:
    - Starts at position (0, 0) on a grid of panels.
    - Faces one of four directions: 0 = up, 1 = right, 2 = down, 3 = left.
    - Paints panels based on instructions and tracks all painted positions.
    """

    def __init__(self, start_color=0):
        self.position = (0, 0)
        self.direction = 0 # 0 = up, 1 = right, 2 = down, 3 = left
        self.panels = defaultdict(int)
        self.panels[self.position] = start_color
        self.painted_positions = set()

    def get_color(self):
        """Returns the color of the current panel (0 = black, 1 = white)."""
        return self.panels[self.position]

    def paint(self, color):
        """Paints the current panel with the specified color and records the position as painted."""
        self.panels[self.position] = color
        self.painted_positions.add(self.position)

    def turn(self, direction):
        """
        Turns the robot 90 degrees left or right.

        Args:
            direction (int): 0 to turn left, 1 to turn right.
        """
        if direction == 0:
            self.direction = (self.direction - 1) % 4
        else:
            self.direction = (self.direction + 1) % 4

    def move(self):
        """Moves the robot forward one panel in the direction it is currently facing."""
        x, y = self.position
        if self.direction == 0:
            self.position = (x, y - 1)
        elif self.direction == 1:
            self.position = (x + 1, y)
        elif self.direction == 2:
            self.position = (x, y + 1)
        elif self.direction == 3:
            self.position = (x - 1, y)


def run_robot(program: List[int], start_color=0) -> Tuple[int, defaultdict]:
    """
    Runs the painting robot using the provided Intcode program.

    The robot starts on a panel with the specified color and follows instructions from the
    Intcode program to paint panels and move around the grid. It stops when the program halts.

    Args:
        program (List[int]): The Intcode program controlling the robot.
        start_color (int, optional): The initial color of the starting panel (0 = black, 1 = white).

    Returns:
        Tuple[int, defaultdict]: A tuple containing:
            - The number of unique panels painted at least once.
            - A defaultdict representing the final panel colors keyed by (x, y) coordinates.
    """
    robot = Robot(start_color)
    computer = IntcodeComputer(program.copy())

    while not computer.halted:
        current_color = robot.get_color()
        computer.add_input(current_color)

        # Get paint instruction from the Intcode program
        paint_color = computer.run()
        if paint_color is None:
            break

        # Get turn instruction (0 = left, 1 = right)
        turn_dir = computer.run()
        if turn_dir is None:
            break

        # Execute the robot's actions
        robot.paint(paint_color)
        robot.turn(turn_dir)
        robot.move()

    return len(robot.painted_positions), robot.panels


def display_panels(panels: defaultdict):
    """
    Displays the painted grid as ASCII art.

    Panels are displayed from top to bottom (increasing Y), and from left to right (increasing X).
    A '#' represents a white panel (color 1), and a space represents a black panel (color 0).

    Args:
        panels (defaultdict): A map of panel positions (x, y) to colors (0 or 1).
    """
    xs = [x for x, _ in panels]
    ys = [y for _, y in panels]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    for y in range(min_y, max_y + 1):
        line = ""
        for x in range(min_x, max_x + 1):
            line += "#" if panels[(x, y)] == 1 else " "
        print(line)


@profiler
def part_one(data_input: List[Tuple[int, int, int]]) -> int:
    """
    Solves part one of the problem using the provided input data.

    Args:
        data_input (List[Tuple[int, int, int]]): A list of tuples representing the positions of the moons.

    Returns:
        int: The total energy of the system after 1000 steps.
    """
    painted_count, _ = run_robot(data_input, start_color=0)
    return painted_count


@profiler
def part_two(data_input: List[Tuple[int, int, int]]) -> None:
    """
    Solves part two of the problem using the provided input data.

    Args:
        data_input (List[Tuple[int, int, int]]): A list of tuples representing the positions of the moons.

    Returns:
        int: The number of steps required for the system to reach a state where all positions and velocities repeat.
    """
    _, final_panels = run_robot(data_input, start_color=1)
    # display_panels(final_panels) # Function that outputs the whole painting.


if __name__ == "__main__":
    input_data = get_input("inputs/11_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    part_two(input_data)
    print("Part 2: UERPRFGJ")
