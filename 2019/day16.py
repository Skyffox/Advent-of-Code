# pylint: disable=line-too-long
"""
Day 16: Flawed Frequency Transmission

Part 1: After 100 phases of FFT, what are the first eight digits in the final output list?
Answer: 84970726

Part 2: After repeating your input signal 10000 times and running 100 phases of FFT, what is the eight-digit message embedded in the final output list?
Answer: 47664469
"""

from typing import List
from utils import profiler


def get_input(file_path: str) -> List[int]:
    """
    Reads the input file and returns a list of digits as integers.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        List[int]: List of digits.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [int(d) for d in file.read().strip()]


def apply_phase(signal: List[int]) -> List[int]:
    """
    Applies one phase of FFT to the signal.

    Args:
        signal (List[int]): Input signal digits.

    Returns:
        List[int]: Transformed signal after one phase.
    """
    base_pattern = [0, 1, 0, -1]
    output = []
    length = len(signal)
    for i in range(length):
        total = 0
        for j in range(length):
            pattern_value = base_pattern[((j + 1) // (i + 1)) % 4]
            total += signal[j] * pattern_value
        output.append(abs(total) % 10)
    return output


@profiler
def part_one(data_input: List[int]) -> int:
    """
    Computes the first 8 digits after 100 FFT phases.

    Args:
        data_input (List[int]): Input signal digits.

    Returns:
        int: First 8 digits as integer.
    """
    signal = data_input.copy()
    for _ in range(100):
        signal = apply_phase(signal)
    return int("".join(map(str, signal[:8])))


@profiler
def part_two(data_input: List[int]) -> int:
    """
    Computes message after 100 phases for a large repeated signal.

    Args:
        data_input (List[int]): Input signal digits.

    Returns:
        int: The 8-digit message embedded in the final output.
    """
    # The offset is given by the first 7 digits
    offset = int("".join(map(str, data_input[:7])))
    # Because offset is in the second half, we can use a trick:
    # The pattern is all zeros then ones, so we only sum suffix
    signal = (data_input * 10000)[offset:]

    for _ in range(100):
        suffix_sum = 0
        for i in range(len(signal) - 1, -1, -1): # Start from the end
            # Compute the new value as the sum of the current digit and the previous accumulated sum
            # Make sure the result fits within a single digit
            suffix_sum = (suffix_sum + signal[i]) % 10
            signal[i] = suffix_sum

    return int("".join(map(str, signal[:8])))


if __name__ == "__main__":
    input_data = get_input("inputs/16_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
