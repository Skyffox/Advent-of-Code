# pylint: disable=line-too-long
"""
Part 1: Check if lists are sorted and whether the pairwise comparison lies within a certain range
Answer: 407

Part 2: Same as part 1, but we may now remove one list entry as a tolerance
Answer: 459
"""

from utils import profiler


def check_safe(report: list) -> bool:
    """Do a pairwise comparison and see if lists are in order"""
    incr = report == sorted(report)
    decr = report == sorted(report, reverse=True)
    return (incr or decr) and all(0 < abs(j - i) < 4 for i, j in zip(report, report[1:]))


def get_input(file_path: str) -> list:
    """Get the input data"""
    with open(file_path, "r", encoding="utf-8") as file:
        return [list(map(int, line.strip().split(" "))) for line in file]


@profiler
def part_1(reports: list) -> int:
    """Check which reports are deemed safe"""
    return sum([check_safe(report) for report in reports])


@profiler
def part_2(reports: list) -> int:
    """Same as part_1() but we may remove a single entry from the list to get a safe report"""
    safe_reports = 0
    for report in reports:
        if check_safe(report):
            safe_reports += 1
        else:
            for idx in range(len(report)):
                # Remove an item from the list, check again, add back if still not valid then repeat
                tmp = report.pop(idx)
                if check_safe(report):
                    safe_reports += 1
                    break
                report.insert(idx, tmp)

    return safe_reports


if __name__ == "__main__":
    # Get input data
    input_data = get_input("inputs/2_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
