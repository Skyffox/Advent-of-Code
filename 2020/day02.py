# pylint: disable=line-too-long
"""
Part 1: Find how many passwords are valid
Answer: 645

Part 2: The password policy was wrong and the first part of the rule was actually the index at which this letter must occur
Answer: 737
"""

from utils import profiler


def get_input(file_path: str) -> list:
    """Get the input data"""
    lst = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip().split(":")

            rule = line[0].split(" ")
            lowerbound, upperbound = rule[0].split("-")
            lowerbound, upperbound = int(lowerbound), int(upperbound)
            password = line[1].strip()

            lst.append([rule, lowerbound, upperbound, password])

    return lst


@profiler
def part_1(lst: list) -> int:
    """Check how many passwords are correct according to their policies"""
    n = 0
    for line in lst:
        rule, lower_b, upper_b, pw = line
        if sum([1 for x in pw if x == rule[1]]) in range(lower_b, upper_b + 1):
            n += 1

    return n


@profiler
def part_2(lst: list) -> int:
    """
    Check if password is correct, the lowerbound and upperbound now represent an index
    in the password and one of them must contain the policy (not both).
    """
    n = 0
    for line in lst:
        rule, lower_b, upper_b, pw = line
        if (pw[lower_b - 1] == rule[1] and pw[lower_b - 1] != pw[upper_b - 1]) or \
           (pw[upper_b - 1] == rule[1] and pw[lower_b - 1] != pw[upper_b - 1]):
            n += 1

    return n


if __name__ == "__main__":
    input_data = get_input("inputs/2_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
