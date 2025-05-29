# pylint: disable=line-too-long
"""
Day 07: Amplification Circuit

Part 1: Try every combination of phase settings on the amplifiers. What is the highest signal that can be sent to the thrusters?
Answer: 440880

Part 2: Try every combination of the new phase settings on the amplifier feedback loop. What is the highest signal that can be sent to the thrusters?
Answer: 3745599
"""

from typing import List
from itertools import permutations
from utils import IntcodeComputer
from utils import profiler


def get_input(file_path: str) -> List[int]:
    """
    Reads the input file and returns a list of stripped lines.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        list[str]: A list of lines with leading/trailing whitespace removed.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return list(map(int, file.read().strip().split(",")))


@profiler
def part_one(program: List[str]) -> int:
    """
    Calculate every combination of phase settings on the amplifiers.

    Args:
        data_input (List[str]): A list of input lines from the puzzle input file.

    Returns:
        int: The highest signal that can be sent to the thrusters.
    """
    max_signal = 0

    for phase_settings in permutations(range(5)):
        signal = 0
        for phase in phase_settings:
            amp = IntcodeComputer(program, [phase, signal])
            signal = amp.run()
        max_signal = max(max_signal, signal)

    return max_signal


@profiler
def part_two(program: List[int]) -> int:
    """
    Finds the maximum output signal from amplifier feedback loop.

    Args:
        program (List[int]): The Intcode program for the amplifiers.

    Returns:
        int: The highest output signal that can be sent to the thrusters.
    """
    max_output = 0

    for phase_setting in permutations(range(5, 10)):
        # Initialize each amplifier with its phase setting
        amplifiers = [IntcodeComputer(program[:], [phase]) for phase in phase_setting]

        signal = 0
        pointer = 0
        last_output = 0

        while not amplifiers[-1].halted:
            amp = amplifiers[pointer % 5]
            amp.add_input(signal)
            output = amp.run()
            if output is not None:
                signal = output
                last_output = signal
            pointer += 1

        max_output = max(max_output, last_output)

    return max_output


if __name__ == "__main__":
    input_data = get_input("inputs/7_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
