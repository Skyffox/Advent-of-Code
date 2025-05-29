# pylint: disable=line-too-long
"""
Day 6: Custom Customs

Part 1: For each group, count the number of questions to which ANYONE answered "yes". What is the sum of those counts?
Answer: 6457

Part 2: For each group, count the number of questions to which EVERYONE answered "yes". What is the sum of those counts?
Answer: 3260
"""

from typing import List
from collections import Counter
from utils import profiler


def get_input(file_path: str) -> List[List[str]]:
    """
    Reads the input file and parses it into a list of groups,
    where each group is a list of strings representing individual answers.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        List[List[str]]: A list of groups, each containing a list of answers.
    """
    groups = []
    group = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:
                group.append(line)
            else:
                groups.append(group)
                group = []

    if group: # Add the last group if the file doesn't end with a blank line
        groups.append(group)

    return groups


@profiler
def part_one(groups: List[str]) -> int:
    """
    Computes the sum of counts of questions to which anyone in each group answered "yes".

    For each group, this function creates a union of all "yes" answers and counts the unique questions.
    The final result is the sum of these counts across all groups.

    Args:
        groups (List[List[str]]): A list where each sublist contains the answers from each person in a group.

    Returns:
        int: The total number of unique "yes" answers across all groups.
    """
    return sum(len(set("".join(group))) for group in groups)


@profiler
def part_two(groups: List[str]) -> int:
    """
    For each group, this function counts how many times each question was answered "yes"
    and includes only those questions answered by all members of the group.

    Args:
        groups (List[List[str]]): A list where each sublist contains the answers from each person in a group.

    Returns:
        int: The total number of questions to which everyone in the group answered "yes", summed across all groups.
    """
    total_count = 0

    for group in groups:
        group_size = len(group)
        group_answers = Counter("".join(group))
        total_count += sum(1 for count in group_answers.values() if count == group_size)

    return total_count


if __name__ == "__main__":
    input_data = get_input("inputs/6_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
