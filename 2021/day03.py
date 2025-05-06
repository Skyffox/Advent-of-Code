# pylint: disable=line-too-long
"""
Day 3: Binary Diagnostic

Part 1: Calculate a real number from the most common/uncommon bits that form a binary number.
Answer: 852500

Part 2: Determine the similarity score between the two lists based on oxygen and CO2 generator ratings.
Answer: 1007985
"""

from typing import List
from utils import profiler


def most_common_bit(lst: List[List[int]], idx: int) -> int:
    """
    Determines the most common bit (0 or 1) at a specific index in a list of binary numbers.

    Args:
        lst (List[List[int]]): A list of binary numbers (each represented as a list of bits).
        idx (int): The index at which to find the most common bit.

    Returns:
        int: The most common bit at the given index (1 for common, 0 for uncommon).
    """
    # Transpose the list so we can easily compare bits at each position
    transposed = list(map(list, zip(*lst)))
    return transposed[idx].count(1) >= transposed[idx].count(0)


def get_input(file_path: str) -> List[List[int]]:
    """
    Reads binary input data from a file and converts it into a list of lists, where each sublist is a binary number.

    Args:
        file_path (str): Path to the input file containing binary numbers.

    Returns:
        List[List[int]]: A list of lists, where each sublist represents a binary number.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [list(map(int, list(line.strip()))) for line in file]


@profiler
def part_1(lst: List[List[int]]) -> int:
    """
    Calculates the power consumption based on the most and least common bits in each position.

    Args:
        lst (List[List[int]]): A list of binary numbers.

    Returns:
        int: The power consumption (gamma rate * epsilon rate).
    """
    gamma_rate, epsilon_rate = 0, 0

    # Transpose the list to easily compare bits in each column
    transposed = list(map(list, zip(*lst)))
    binary_lst = [bit.count(1) > bit.count(0) for bit in transposed]

    # Convert the most common bits (gamma rate) and least common bits (epsilon rate) to decimal values
    for idx, binary in enumerate(binary_lst[::-1]):
        if binary == 1:
            gamma_rate += 2**idx
        else:
            epsilon_rate += 2**idx

    return gamma_rate * epsilon_rate


@profiler
def part_2(lst: List[List[int]]) -> int:
    """
    Finds the oxygen generator rating and CO2 scrubber rating by filtering on the most and least common bits 
    at each index and then multiplying the two ratings together.

    Args:
        lst (List[List[int]]): A list of binary numbers.

    Returns:
        int: The product of the oxygen generator rating and CO2 scrubber rating.
    """
    oxygen_generator, co2_scrubber = lst[::], lst[::]
    i = 0
    # Find the oxygen generator rating
    while len(oxygen_generator) != 1:
        bit = most_common_bit(oxygen_generator, i)
        oxygen_generator = [l for l in oxygen_generator if l[i] == bit]
        i += 1

    i = 0
    # Find the CO2 scrubber rating
    while len(co2_scrubber) != 1:
        bit = most_common_bit(co2_scrubber, i)
        co2_scrubber = [l for l in co2_scrubber if l[i] != bit]
        i += 1

    # Convert the binary numbers to decimal
    oxygen_real = sum([2**idx if b == 1 else 0 for idx, b in enumerate(oxygen_generator[0][::-1])])
    co2_real = sum([2**idx if b == 1 else 0 for idx, b in enumerate(co2_scrubber[0][::-1])])

    return oxygen_real * co2_real


if __name__ == "__main__":
    input_data = get_input("inputs/3_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
