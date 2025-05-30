# pylint: disable=line-too-long
"""
Day 09: Sensor Boost

Part 1: What BOOST keycode does it produce?
Answer: 3497884671

Part 2: Run the BOOST program in sensor boost mode. What are the coordinates of the distress signal?
Answer: 46470
"""

from typing import List
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


@profiler
def run_boost_diagnostic(program: List[int], input_value: int) -> int:
    """
    Runs the Intcode program in BOOST mode using the provided input value
    and returns the final diagnostic output.

    Args:
        program (List[int]): The Intcode program to execute.
        input_value (int): Input value for the BOOST system (1 for test mode, 2 for keycode mode).

    Returns:
        int: The final output value produced by the program.
    """
    computer = IntcodeComputer(program.copy())
    computer.add_input(input_value)
    output = None

    while not computer.halted:
        val = computer.run()
        if val is not None:
            output = val

    return output


if __name__ == "__main__":
    input_data = get_input("inputs/9_input.txt")

    print(f"Part 1: {run_boost_diagnostic(input_data, 1)}")
    print(f"Part 2: {run_boost_diagnostic(input_data, 2)}")
