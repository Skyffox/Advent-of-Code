# pylint: disable=line-too-long
"""
Day 2: Red-Nosed Reports

Part 1: Check if lists are sorted and whether the pairwise comparison lies within a certain range
Answer: 407

Part 2: Same as part 1, but we may now remove one list entry as a tolerance
Answer: 459
"""

from typing import List
from utils import profiler


def check_safe(report: List[int]) -> bool:
    """
    Check if a report is safe.
    A report is considered safe if it is entirely increasing or decreasing,
    and each adjacent pair has an absolute difference between 1 and 3 (exclusive).

    Args:
        report (List[int]): A list of integer values in a report.

    Returns:
        bool: True if the report is safe, False otherwise.
    """
    incr = report == sorted(report)
    decr = report == sorted(report, reverse=True)
    return (incr or decr) and all(0 < abs(j - i) < 4 for i, j in zip(report, report[1:]))


def get_input(file_path: str) -> List[List[int]]:
    """
    Parse the input file into a list of reports.

    Each line in the file should contain space-separated integers,
    which will be parsed into a list.

    Args:
        file_path (str): Path to the input file.

    Returns:
        List[List[int]]: A list of integer lists (reports).
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [list(map(int, line.strip().split(" "))) for line in file]


@profiler
def part_1(reports: List[List[int]]) -> int:
    """
    Count how many reports are safe.

    Args:
        reports (List[List[int]]): A list of reports to evaluate.

    Returns:
        int: The number of safe reports.
    """
    return sum(check_safe(report) for report in reports)


@profiler
def part_2(reports: List[List[int]]) -> int:
    """
    Count how many reports can be made safe by removing at most one entry.

    Args:
        reports (List[List[int]]): A list of reports to evaluate.

    Returns:
        int: The number of reports that are safe or can be made safe.
    """
    safe_reports = 0
    for report in reports:
        if check_safe(report):
            safe_reports += 1
        else:
            for idx in range(len(report)):
                # Remove an item from the list, check again, break if valid
                modified = report[:idx] + report[idx+1:]
                if check_safe(modified):
                    safe_reports += 1
                    break

    return safe_reports


if __name__ == "__main__":
    input_data = get_input("inputs/2_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
