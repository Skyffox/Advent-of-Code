# pylint: disable=line-too-long
"""
Day 13: Shuttle Search

Part 1: What is the ID of the earliest bus you can take to the airport multiplied by the number of minutes you'll need to wait for that bus?
Answer: 222

Part 2: What is the earliest timestamp such that all of the listed bus IDs depart at offsets matching their positions in the list?
Answer: 1068781
"""

from typing import List
from utils import profiler


def get_input(file_path: str) -> List[str]:
    """
    Reads the input file and returns a list of stripped lines.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        list[str]: A list of lines with leading/trailing whitespace removed.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file.readlines()]


@profiler
def part_one(data_input: List[str]) -> int:
    """
    Finds the earliest bus you can take after the given departure time,
    and returns the product of the bus ID and your waiting time.

    Args:
        data_input (List[str]): Input list where
            - data_input[0] is your earliest departure time (as a string).
            - data_input[1] is a comma-separated list of bus IDs or 'x'.

    Returns:
        int: The product of the earliest bus ID you can take and the minutes you wait.
    """
    departure_time = int(data_input[0])
    bus_ids = [int(bus_id) for bus_id in data_input[1].split(",") if bus_id != "x"]
    wait_times = [(bus_id - departure_time % bus_id, bus_id) for bus_id in bus_ids]
    wait_time, bus_id = min(wait_times)
    return wait_time * bus_id


@profiler
def part_two(data_input: List[str]) -> int:
    """
    Finds the earliest timestamp such that all listed bus IDs depart at offsets matching their positions.

    This solves a system of modular equations using the Chinese Remainder Theorem approach:
    For each bus with ID `bus_id` at index `offset`, the timestamp satisfies:
        (timestamp + offset) % bus_id == 0

    Args:
        data_input (List[str]): Input list where
            - data_input[1] is a comma-separated list of bus IDs or 'x'.

    Returns:
        int: The earliest timestamp meeting the schedule conditions.
    """
    bus_schedule = [
        (int(bus_id), offset)
        for offset, bus_id in enumerate(data_input[1].split(","))
        if bus_id != "x"
    ]
    timestamp = 0
    step = 1
    for bus_id, offset in bus_schedule:
        while (timestamp + offset) % bus_id != 0:
            timestamp += step
        step *= bus_id # Increment step by multiplying by bus_id to keep conditions valid
    return timestamp


if __name__ == "__main__":
    input_data = get_input("inputs/13_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
