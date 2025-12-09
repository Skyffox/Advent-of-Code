# pylint: disable=line-too-long
"""
Day 3 Challenge: Lobby 

Part 1: A bank is a line of numbers in input, the joltage that the bank produces is equal to the number formed by the digits on the batteries you've turned on.
For each bank what is the total output joltage.
Answer: 17443

Part 2: Do the same as part 1, but instead of turning on 2 batteries now turn on 12.
Answer: 172167155440541
"""

from typing import List
from utils import profiler


def get_input(file_path: str) -> List[List[str]]:
    """
    Parse the input file into banks of battery digits.

    Each line of the input represents a bank, containing digit characters (0–9).
    The result is a list of banks, where each bank is a list of digit strings.

    Args:
        file_path (str): Path to the input file.

    Returns:
        List[List[str]]: A list of banks, each being a list of digit characters.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [list(line.strip()) for line in file]


@profiler
def part_one(data_input: List[List[str]]) -> int:
    """
    Compute the total joltage from all banks.

    For a single bank:  
    - Consider every pair of digits (i, j) with i < j.  
    - Form the two-digit number: int(digit[i] + digit[j]).  
    - The bank's joltage is the maximum found in the bank.

    Args:
        data_input (List[List[str]]): Parsed input where each element is a list
                                      of digit characters representing a bank.

    Returns:
        int: The sum of the maximum two-digit numbers producible from each bank.
    """
    max_voltage = 0
    for digits in data_input:
        max_battery_voltage = 0
        n = len(digits)
        for i in range(n - 1):
            d1 = digits[i]
            for d2 in digits[i + 1:]:
                max_battery_voltage = max(max_battery_voltage, int(d1 + d2))

        max_voltage += max_battery_voltage
    return max_voltage


@profiler
def part_two(data_input: List[List[str]]) -> int:
    """
    Construct the maximum possible number from each bank using an ordered greedy selection.

    The process for a single bank is:
    - Build a new sequence of the same length as the original.
    - At each step, among all digits that can still form a full-length sequence, pick the largest possible digit.
    - Continue scanning from just after the chosen digit.

    After constructing this maximal number for each bank, convert it to an integer
    and sum all results.

    Args:
        data_input (List[List[str]]): Parsed input where each element represents
                                      a bank of digit characters.

    Returns:
        int: The sum of the maximal reconstructed numbers.
    """
    max_voltage = 0
    for digits in data_input:
        max_battery_voltage = []
        lower = 0
        n = len(digits)

        # Number of digits remaining to select decreases each iteration.
        for remaining in range(11, -1, -1):
            # The valid region ends at a point that still leaves enough digits
            upper = n - remaining

            segment = digits[lower:upper]
            highest_digit = max(segment)
            # Find next lower bound by finding the index of the new highest number
            # Add index of previous lower bound and add 1 to prepare for next iteration.
            lower = segment.index(highest_digit) + lower + 1
            max_battery_voltage.append(highest_digit)

        max_voltage += int("".join(max_battery_voltage))

    return max_voltage


if __name__ == "__main__":
    # Get input data
    input_data = get_input("inputs/3_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
