# pylint: disable=line-too-long
"""
Day 4: Repose Record

Part 1: Strategy 1: Find the guard that has the most minutes asleep. What minute does that guard spend asleep the most?
Answer: 19830

Part 2: Strategy 2: Of all guards, which guard is most frequently asleep on the same minute?
Answer: 43695
"""

from typing import Tuple, Dict, List
from collections import defaultdict
import re
from datetime import datetime
from utils import profiler


def read_parse_and_process(file_path: str) -> Tuple[Dict[int, List[int]], Dict[int, int]]:
    """
    Reads the input file, parses each line into events, sorts them by timestamp,
    and processes logs to calculate guard sleep patterns.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        Tuple[dict, dict]: 
            - guard_sleep: dict with guard IDs as keys and lists of minute counts asleep.
            - guard_totals: dict with guard IDs as keys and total minutes asleep.
    """
    parsed_logs = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            timestamp_str, event = line[1:17], line[19:]
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M")
            guard_match = re.match(r"Guard #(\d+) begins shift", event)
            guard_id = int(guard_match.group(1)) if guard_match else None
            parsed_logs.append((timestamp, guard_id, event))

    # Sort by timestamp
    parsed_logs.sort(key=lambda x: x[0])

    guard_sleep = defaultdict(lambda: [0] * 60)
    guard_totals = defaultdict(int)
    current_guard = None
    sleep_start = None

    for timestamp, guard_id, event in parsed_logs:
        if guard_id is not None:
            current_guard = guard_id
        elif event == "falls asleep":
            sleep_start = timestamp.minute
        elif event == "wakes up":
            for minute in range(sleep_start, timestamp.minute):
                guard_sleep[current_guard][minute] += 1
            guard_totals[current_guard] += timestamp.minute - sleep_start

    return guard_sleep, guard_totals


@profiler
def part_one(guard_sleep: dict, guard_totals: dict) -> int:
    """
    Find the guard with the most total minutes asleep, and the minute they are most asleep.

    Args:
        guard_sleep (dict): Guard sleep data (guard_id -> list of minute counts).
        guard_totals (dict): Total sleep per guard (guard_id -> total minutes asleep).

    Returns:
        int: guard ID multiplied by the minute they are asleep the most.
    """
    sleepiest_guard = max(guard_totals, key=guard_totals.get)
    sleepiest_minute = guard_sleep[sleepiest_guard].index(max(guard_sleep[sleepiest_guard]))
    return sleepiest_guard * sleepiest_minute


@profiler
def part_two(guard_sleep: dict) -> int:
    """
    Find the guard most frequently asleep on the same minute.

    Args:
        guard_sleep (dict): Guard sleep data (guard_id -> list of minute counts).

    Returns:
        int: guard ID multiplied by the minute they are asleep the most frequently.
    """
    most_frequent_guard, most_frequent_minute = max(
        ((guard, minute) for guard, minutes in guard_sleep.items()
         for minute, count in enumerate(minutes) if count > 0),
        key=lambda x: guard_sleep[x[0]][x[1]]
    )
    return most_frequent_guard * most_frequent_minute


if __name__ == "__main__":
    sleep, total = read_parse_and_process("inputs/4_input.txt")

    print(f"Part 1: {part_one(sleep, total)}")
    print(f"Part 2: {part_two(sleep)}")