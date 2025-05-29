# pylint: disable=line-too-long
"""
Day 8: Two-Factor Authentication

Part 1: There seems to be an intermediate check of the voltage used by the display: after you swipe your card, if the screen did work, how many pixels should be lit?
Answer: 110

Part 2: After you swipe your card, what code is the screen trying to display?
Answer: See printed screen output (zjhrkcplyj)

"""

from typing import List
from utils import profiler


class Screen:
    """
    Represents a 2D pixel screen where each pixel can be either on (True) or off (False).
    
    Provides methods to draw rectangles, rotate rows and columns, count lit pixels,
    and display the screen state.
    """

    def __init__(self, width: int, height: int):
        """
        Initializes the screen with given width and height.

        Args:
            width (int): Number of columns (pixels per row).
            height (int): Number of rows (pixels per column).
        """
        self.width = width
        self.height = height
        self.pixels = [[False] * width for _ in range(height)]

    def rect(self, a: int, b: int):
        """
        Turns on all pixels in a rectangle starting from the top-left corner (0,0)
        with width 'a' and height 'b'.

        Args:
            a (int): Width of the rectangle.
            b (int): Height of the rectangle.
        """
        for y in range(b):
            for x in range(a):
                self.pixels[y][x] = True

    def rotate_row(self, y: int, by: int):
        """
        Rotates the pixels in row 'y' to the right by 'by' positions.

        Args:
            y (int): The index of the row to rotate.
            by (int): Number of positions to rotate.
        """
        by %= self.width
        self.pixels[y] = self.pixels[y][-by:] + self.pixels[y][:-by]

    def rotate_column(self, x: int, by: int):
        """
        Rotates the pixels in column 'x' downward by 'by' positions.

        Args:
            x (int): The index of the column to rotate.
            by (int): Number of positions to rotate.
        """
        by %= self.height
        col = [self.pixels[y][x] for y in range(self.height)]
        col = col[-by:] + col[:-by]
        for y in range(self.height):
            self.pixels[y][x] = col[y]

    def count_lit(self) -> int:
        """
        Counts the number of pixels that are currently turned on.

        Returns:
            int: The total number of lit (True) pixels.
        """
        return sum(sum(row) for row in self.pixels)

    def display(self):
        """
        Displays the current state of the screen in the terminal,
        with '#' representing lit pixels and ' ' representing unlit pixels.
        """
        for row in self.pixels:
            print("".join("#" if pixel else " " for pixel in row))


def get_input(file_path: str) -> List[str]:
    """
    Reads the input file and returns a list of stripped instruction lines.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        list[str]: List of instructions.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file]


@profiler
def compute(data_input: List[str]) -> int:
    """
    Executes all instructions on the screen and returns the count of lit pixels.

    Args:
        data_input (List[str]): List of instructions.

    Returns:
        int: Number of lit pixels after executing instructions.
    """
    screen = Screen(50, 6)
    for line in data_input:
        if line.startswith("rect"):
            a, b = map(int, line[5:].split('x'))
            screen.rect(a, b)
        elif line.startswith("rotate row"):
            parts = line.split()
            y = int(parts[2].split('=')[1])
            by = int(parts[-1])
            screen.rotate_row(y, by)
        elif line.startswith("rotate column"):
            parts = line.split()
            x = int(parts[2].split('=')[1])
            by = int(parts[-1])
            screen.rotate_column(x, by)

    return screen


if __name__ == "__main__":
    input_data = get_input("inputs/8_input.txt")

    pixels = compute(input_data)

    print(f"Part 1: {pixels.count_lit()}")
    print("Part 2: ZJHRKCPLYJ")
    pixels.display()
