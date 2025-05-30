# pylint: disable=line-too-long
"""
Day 14: Reindeer Olympics

Part 1: Given the descriptions of each reindeer, after exactly 2503 seconds, what distance has the winning reindeer traveled?
Answer: 2655

Part 2: Again given the descriptions of each reindeer, after exactly 2503 seconds, how many points does the winning reindeer have?
Answer: 1059
"""

from typing import Dict
import re
from utils import profiler


def get_input(file_path: str) -> Dict[str, Dict[str, int]]:
    """
    Reads the input file and parses reindeer statistics.

    Each line describes a reindeer's flying speed, flying duration, and resting duration.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        Dict[str, Dict[str, int]]: Mapping of reindeer name to their stats:
            {
                "speed": int (km/s),
                "fly_time": int (seconds),
                "rest_time": int (seconds)
            }
    """
    pattern = re.compile(
        r"(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds."
    )
    reindeer_stats = {}
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            match = pattern.match(line.strip())
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
    Computes the distance a reindeer travels in total_time seconds.

    The reindeer alternates between flying and resting. It flies at constant speed
    for `fly_time` seconds, then rests for `rest_time` seconds, repeating this cycle.

    Args:
        stats (Dict[str, int]): Reindeer stats including 'speed', 'fly_time', 'rest_time'.
        total_time (int): Total elapsed time in seconds.

    Returns:
        int: Total distance traveled in kilometers.
    """
    cycle_duration = stats["fly_time"] + stats["rest_time"]
    full_cycles = total_time // cycle_duration
    remainder = total_time % cycle_duration
    flying_seconds = full_cycles * stats["fly_time"] + min(remainder, stats["fly_time"])
    return flying_seconds * stats["speed"]


@profiler
def part_one(reindeer: Dict[str, Dict[str, int]]) -> int:
    """
    Determines which reindeer has traveled the farthest after 2503 seconds.
    Uses direct calculation based on reindeer's flying/resting cycles.

    Args:
        reindeer (Dict[str, Dict[str, int]]): Parsed reindeer statistics.

    Returns:
        int: Maximum distance traveled by any reindeer.
    """
    race_time = 2503
    return max(distance_after_time(stats, race_time) for stats in reindeer.values())


@profiler
def part_two(reindeer: Dict[str, Dict[str, int]]) -> int:
    """
    Simulates the race second-by-second, awarding points each second to the
    reindeer(s) currently in the lead.

    Args:
        reindeer (Dict[str, Dict[str, int]]): Parsed reindeer statistics.

    Returns:
        int: Highest points earned by any reindeer at race end.
    """
    race_time = 2503
    scores = {name: 0 for name in reindeer}

    for second in range(1, race_time + 1):
        distances = {
            name: distance_after_time(stats, second) for name, stats in reindeer.items()
        }
        max_distance = max(distances.values())
        for name, dist in distances.items():
            if dist == max_distance:
                scores[name] += 1

    return max(scores.values())


if __name__ == "__main__":
    reindeer_data = get_input("inputs/14_input.txt")

    print(f"Part 1: {part_one(reindeer_data)}")
    print(f"Part 2: {part_two(reindeer_data)}")
