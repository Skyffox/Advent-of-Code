# pylint: disable=line-too-long
"""
Day 4: Repose Record

Part 1: Strategy 1: Find the guard that has the most minutes asleep. What minute does that guard spend asleep the most?
Answer: 19830

Part 2: Strategy 2: Of all guards, which guard is most frequently asleep on the same minute?
Answer: 43695
"""

from typing import List
from collections import defaultdict
import re
from datetime import datetime
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
        return [line.strip() for line in file]


def parse_event(line: str):
    """
    Parses a log line into a tuple of timestamp, guard ID (if any), and event type.

    Args:
        line (str): A single line from the log file.

    Returns:
        tuple: (datetime, guard_id (int or None), event_type (str))
    """
    timestamp_str, event = line[1:17], line[19:]
    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M")
    guard_match = re.match(r"Guard #(\d+) begins shift", event)
    guard_id = int(guard_match.group(1)) if guard_match else None
    return timestamp, guard_id, event


def process_logs(logs: List[str]):
    """
    Processes the sorted logs to calculate sleep patterns.

    Args:
        logs (List[str]): Sorted list of log entries.

    Returns:
        dict: Guard sleep data with guard IDs as keys and sleep minute counts as values.
    """
    guard_sleep = defaultdict(lambda: [0] * 60)
    guard_totals = defaultdict(int)
    current_guard = None
    sleep_start = None

    for timestamp, guard_id, event in map(parse_event, logs):
        if guard_id:
            current_guard = guard_id
        elif event == "falls asleep":
            sleep_start = timestamp.minute
        elif event == "wakes up":
            for minute in range(sleep_start, timestamp.minute):
                guard_sleep[current_guard][minute] += 1
            guard_totals[current_guard] += timestamp.minute - sleep_start

    return guard_sleep, guard_totals


@profiler
def part_one(data_input: List[str]) -> int:
    """
    Find the guard that has the most minutes asleep and find what minute does that guard spend asleep the most.

    Args:
        data_input (List[str]): A list of input lines from the puzzle input file.

    Returns:
        int: the ID of the guard times the minute he is asleep the most
    """
    logs = sorted(data_input)
    guard_sleep, guard_totals = process_logs(logs)

    # Find the guard with the most total sleep
    sleepiest_guard = max(guard_totals, key=guard_totals.get)
    # Find the minute the sleepiest guard is most often asleep
    sleepiest_minute = guard_sleep[sleepiest_guard].index(max(guard_sleep[sleepiest_guard]))
    return sleepiest_guard * sleepiest_minute


@profiler
def part_two(data_input: List[str]) -> int:
    """
    Of all guards, which guard is most frequently asleep on the same minute?
    
    Args:
        data_input (List[str]): A list of input lines from the puzzle input file.

    Returns:
        int: the ID of the guard times the minute he is asleep the most
    """
    logs = sorted(data_input)
    guard_sleep, _ = process_logs(logs)

    # Find the guard and minute with the most frequent sleep
    most_frequent_guard, most_frequent_minute = max(
        ((guard, minute) for guard, minutes in guard_sleep.items()
         for minute, count in enumerate(minutes) if count > 0),
        key=lambda x: guard_sleep[x[0]][x[1]]
    )
    return most_frequent_guard * most_frequent_minute


if __name__ == "__main__":
    input_data = get_input("inputs/4_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
