# pylint: disable=line-too-long
"""
Day 05: Sunny with a Chance of Asteroids

Part 1: After providing 1 to the only input instruction and passing all the tests, what diagnostic code does the program produce?
Answer: 4511442

Part 2: What is the diagnostic code for system ID 5?
Answer: 12648139
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
def run_diagnostic(program: List[int], system_id: int) -> int:
    """
    Runs the Intcode program with the specified system ID as input and returns the diagnostic code.

    Args:
        program (List[int]): The Intcode program.
        system_id (int): The input value to provide to the program (system ID).

    Returns:
        int: The diagnostic code output produced by the program.
    """
    computer = IntcodeComputer(program.copy())
    computer.add_input(system_id)
    output = None
    while not computer.halted:
        val = computer.run()
        if val is not None:
            output = val # Keep track of the last output before halt
    return output


if __name__ == "__main__":
    input_data = get_input("inputs/5_input.txt")

    print(f"Part 1: {run_diagnostic(input_data, system_id=1)}")
    print(f"Part 2: {run_diagnostic(input_data, system_id=5)}")
