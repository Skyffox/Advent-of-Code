# pylint: disable=line-too-long
"""
Day 15: Rambunctious Recitation

Part 1: Given your starting numbers, what will be the 2020th number spoken?
Answer: 1428

Part 2: Given your starting numbers, what will be the 30000000th number spoken?
Answer: 3718541

"""

from typing import List
from utils import profiler


def get_input(file_path: str) -> List[int]:
    """
    Reads the input file and returns a list of integers.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        list[int]: List of starting numbers.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [int(x) for x in file.read().strip().split(",")]


@profiler
def play_memory_game(starting_numbers: List[int], target_turn: int) -> int:
    """
    Plays the memory game until the target turn and returns the last spoken number.

    Args:
        starting_numbers (list[int]): The starting numbers.
        target_turn (int): The turn to stop at.

    Returns:
        int: The number spoken at the target turn.
    """
    last_seen = {num: i + 1 for i, num in enumerate(starting_numbers[:-1])}
    last_number = starting_numbers[-1]

    for turn in range(len(starting_numbers), target_turn):
        if last_number in last_seen:
            next_number = turn - last_seen[last_number]
        else:
            next_number = 0
        last_seen[last_number] = turn
        last_number = next_number

    return last_number


if __name__ == "__main__":
    input_data = get_input("inputs/15_input.txt")

    print(f"Part 1: {play_memory_game(input_data, 2020)}")
    print(f"Part 2: {play_memory_game(input_data, 30000000)}")
