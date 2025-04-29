# pylint: disable=line-too-long
"""
Part 1: In how many assignment pairs does one range fully contain the other?
Answer: 644

Part 2: In how many assignment pairs do the ranges overlap?
Answer: 926
"""

from utils import profiler


def get_input(file_path: str) -> list:
    """Get the input data"""
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip().split(",") for line in file]


@profiler
def part_1(assignments: list) -> int:
    """See if either range fits into the other one"""
    count = 0
    for line in assignments:
        r1, r2 = line[0].split("-"), line[1].split("-")

        if int(r1[0]) >= int(r2[0]) and int(r1[1]) <= int(r2[1]) or \
           int(r2[0]) >= int(r1[0]) and int(r2[1]) <= int(r1[1]):
            count += 1

    return count


@profiler
def part_2(assignments: list) -> int:
    """Instead of counting full overlap like in part 1 we count partial overlap"""
    count = 0
    for line in assignments:
        r1, r2 = line[0].split("-"), line[1].split("-")

        for r in range(int(r1[0]), int(r1[1]) + 1):
            if r in range(int(r2[0]), int(r2[1]) + 1):
                count += 1
                break

    return count


if __name__ == "__main__":
    input_data = get_input("inputs/4_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
