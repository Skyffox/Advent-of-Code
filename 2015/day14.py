# pylint: disable=line-too-long
"""
Day 14: Reindeer Olympics

Part 1: Given the descriptions of each reindeer, after exactly 2503 seconds, what distance has the winning reindeer traveled?
Answer: 2655

Part 2: Again given the descriptions of each reindeer, after exactly 2503 seconds, how many points does the winning reindeer have?
Answer: 1059
"""

from typing import List, Dict
import re
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


def parse_reindeer(data: List[str]) -> Dict[str, Dict[str, int]]:
    """
    Parses each reindeer's stats: speed, fly time, rest time.

    Args:
        data (List[str]): Input lines describing reindeer capabilities.

    Returns:
        Dict[str, Dict[str, int]]: Mapping reindeer name to their stats.
    """
    pattern = re.compile(
        r"(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds."
    )
    reindeer_stats = {}
    for line in data:
        match = pattern.match(line)
        if match:
            name, speed, fly_time, rest_time = match.groups()
            reindeer_stats[name] = {
                "speed": int(speed),
                "fly_time": int(fly_time),
                "rest_time": int(rest_time),
            }
    return reindeer_stats


def distance_after_time(stats: Dict[str, int], total_time: int) -> int:
    """
    Calculates distance traveled by a reindeer after given total time.

    Args:
        stats (Dict[str, int]): Dictionary with speed, fly_time, rest_time.
        total_time (int): Total race time in seconds.

    Returns:
        int: Distance traveled.
    """
    cycle_time = stats["fly_time"] + stats["rest_time"]
    full_cycles = total_time // cycle_time
    remainder = total_time % cycle_time
    flying_time = full_cycles * stats["fly_time"] + min(remainder, stats["fly_time"])
    return flying_time * stats["speed"]


@profiler
def part_one(data_input: List[str]) -> int:
    """
    Determines the maximum distance traveled by any reindeer after 2503 seconds.

    Args:
        data_input (List[str]): Input lines describing reindeer capabilities.

    Returns:
        int: Maximum distance traveled.
    """
    reindeer = parse_reindeer(data_input)
    race_time = 2503
    distances = [distance_after_time(stats, race_time) for stats in reindeer.values()]
    return max(distances)


@profiler
def part_two(data_input: List[str]) -> int:
    """
    Simulates the race second-by-second and awards points for leading reindeer.

    Args:
        data_input (List[str]): Input lines describing reindeer capabilities.

    Returns:
        int: Maximum points earned by any reindeer.
    """
    reindeer = parse_reindeer(data_input)
    race_time = 2503
    scores = {name: 0 for name in reindeer}

    for t in range(1, race_time + 1):
        distances = {
            name: distance_after_time(stats, t) for name, stats in reindeer.items()
        }
        max_dist = max(distances.values())
        for name, dist in distances.items():
            if dist == max_dist:
                scores[name] += 1

    return max(scores.values())


if __name__ == "__main__":
    input_data = get_input("inputs/14_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
