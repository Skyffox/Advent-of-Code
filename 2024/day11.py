# pylint: disable=line-too-long
"""
Day 11: Plutonian Pebbles

Part 1: How many stones will you have after blinking 25 times?
Answer: 172484

Part 2: How many stones will you have after blinking 75 times?
Answer: 205913561055242
"""

from typing import List, Dict
from utils import profiler


def get_input(file_path: str) -> List[int]:
    """
    Read the initial list of pebble values from an input file.

    The input file contains a single line of space-separated integers.
    Each integer represents the value of a unique starting stone.

    Args:
        file_path (str): Path to the input file.

    Returns:
        list[int]: List of integer stone values.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return list(map(int, file.readlines()[0].split(" ")))


def blink(my_dict: Dict[int, int]) -> Dict[int, int]:
    """
    Simulate a single "blink" transformation step on a collection of stones.

    Each stone value is processed according to the following rules:
    - If the value is 0 → it becomes 1.
    - If the length of the current value is divisible by 2 → then 2 new stones will have the value of either side of the current value
    - If the number of digits is odd → the value is multiplied by 2024.

    Stones are tracked in a dictionary to count duplicates without tracking individual objects.

    Args:
        my_dict (dict[int, int]): Dictionary where keys are stone values and values are the count of those stones.

    Returns:
        dict[int, int]: New dictionary representing the result of applying one blink to all stones.
    """
    new_dict: Dict[int, int] = {}
    for key, val in my_dict.items():
        if key == 0:
            new_dict[1] = new_dict.get(1, 0) + val
        elif len(str(key)) % 2 == 0:
            left = int(str(key)[len(str(key)) // 2:])
            right = int(str(key)[:len(str(key)) // 2])

            new_dict[left] = new_dict.get(left, 0) + val
            new_dict[right] = new_dict.get(right, 0) + val
        else:
            new_val = key * 2024
            new_dict[new_val] = new_dict.get(new_val, 0) + val

    return new_dict


@profiler
def compute(data_input: List[int], nr_blinks: int) -> int:
    """
    Simulate the blinking process for all stones a given number of times.

    Each stone in the input list is treated independently. The function applies
    the blink transformation `nr_blinks` times to each stone, and then counts the total number of stones produced.

    Args:
        data_input (list[int]): List of starting stone values.
        nr_blinks (int): The number of times to apply the blink process.

    Returns:
        int: The total number of stones after all blinks have been applied.
    """
    n: int = 0
    for num in data_input:
        stones: Dict[int, int] = {num: 1}
        for _ in range(nr_blinks):
            stones = blink(stones)
        n += sum(stones.values())

    return n


if __name__ == "__main__":
    input_data: List[int] = get_input("inputs/11_input.txt")

    print(f"Part 1: {compute(input_data, 25)}")
    print(f"Part 2: {compute(input_data, 75)}")
