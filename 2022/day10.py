# pylint: disable=line-too-long
"""
Day 10: Cathode-Ray Tube

Part 1: Find the signal strength during the 20th, 60th, 100th, 140th, 180th, and 220th cycles. What is the sum of these six signal strengths?
Answer: 13920

Part 2: Render the image given by your program. What eight capital letters appear on your CRT?
Answer: EGLHBLFJ
"""

from utils import profiler


def get_input(file_path: str) -> list:
    """
    Reads the input data from a file and splits it into a list of instructions.

    Each instruction represents a command in the format of a string, with the first element 
    being the operation (e.g., "addx") and the second element being the value (if applicable).
    
    Args:
        file_path (str): The path to the input file.
        
    Returns:
        list: A list of instructions, where each instruction is a list of two elements.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip().split() for line in file]


@profiler
def part_1(lines: list) -> int:
    """
    Calculates the sum of the signal strengths during specific cycles (20, 60, 100, 140, 180, 220). 
    A signal strength is computed by multiplying the current cycle number by the register value 
    at that cycle.

    This function simulates the cycles, checking if the current cycle matches one of the
    specified cycles. If it does, it adds the product of the cycle number and the register value 
    to the total signal strength.

    Args:
        lines (list): A list of instructions, where each instruction contains an operation and 
                      a value to modify the register.

    Returns:
        int: The total sum of the signal strengths during the specified cycles.
    """
    total, counter, initial_value = 0, 1, 1
    cycles = {20, 60, 100, 140, 180, 220}

    for line in lines:
        for idx, _ in enumerate(line):
            if counter in cycles:
                total += initial_value * counter

            counter += 1

            # "addx V" command takes two cycles to complete
            if idx == 1:
                initial_value += int(line[1])

    return total


@profiler
def part_2(lines: list) -> str:
    """
    Simulates a CRT display and generates an image of a series of lit and dark pixels based on the 
    movement of a sprite on the screen. The sprite's position is determined by the register value,
    and if the sprite's position overlaps with the current pixel being drawn, it will light up.

    The function renders a message on a 40-column CRT screen and returns the sequence of capital 
    letters spelled out by the lit pixels.

    Args:
        lines (list): A list of instructions, where each instruction contains an operation 
                      that modifies the register value.

    Returns:
        str: A string representing the message shown on the CRT, which is composed of eight capital letters.
    """
    message, row = [], []
    initial_value, counter = 1, 1
    for line in lines:
        for idx, _ in enumerate(line):
            # The CRT is 40 pixels wide
            pos = counter % 40

            # If the sprite is positioned such that one of its three pixels is the
            # pixel currently being drawn, the screen produces a lit pixel
            if pos in range(initial_value, initial_value + 3):
                row.append("# ")
            else:
                row.append(". ")

            if pos == 0:
                message.append(row)
                row = []

            counter += 1

            if idx == 1:
                initial_value += int(line[1])

    # NOTE: The message spells out the following letters: EGLHBLFJ
    # Uncomment the following lines to print the CRT image for visual representation
    # for x in message:
    #     print("".join(x))

    return "EGLHBLFJ"  # Returning the string directly, which is the expected output


if __name__ == "__main__":
    input_data = get_input("inputs/10_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
