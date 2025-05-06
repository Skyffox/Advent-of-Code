# pylint: disable=line-too-long
"""
Day 2: Password Philosophy

Part 1: Find how many passwords are valid according to the given policy.
Answer: 645

Part 2: The password policy was wrong, and the first part of the rule was actually the index at which this letter must occur.
Answer: 737
"""

from typing import List, Tuple
from utils import profiler


def get_input(file_path: str) -> List[Tuple[List[str], int, int, str]]:
    """
    Read the input file and parse the data into a list of password policies and passwords.

    Args:
        file_path (str): Path to the input file.

    Returns:
        List[Tuple[List[str], int, int, str]]: A list where each element contains:
            - The rule as a list [lower-upper range, letter to check]
            - The lower bound integer
            - The upper bound integer
            - The password string
    """
    lst = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip().split(":")

            # Extract rule and split into lowerbound, upperbound and letter
            rule = line[0].split(" ")
            lowerbound, upperbound = map(int, rule[0].split("-"))            
            password = line[1].strip()

            lst.append([rule, lowerbound, upperbound, password])

    return lst


@profiler
def part_1(lst: List[Tuple[List[str], int, int, str]]) -> int:
    """
    Validate passwords according to the policy where the number of occurrences of the letter
    in the password must be within the specified range (inclusive).

    Args:
        lst (List[Tuple[List[str], int, int, str]]): List of tuples where each tuple contains:
            - Rule, lower bound, upper bound, password
            
    Returns:
        int: The number of valid passwords according to the policy.
    """
    valid_count = 0
    for rule, lower_b, upper_b, password in lst:
        letter = rule[1]
        if lower_b <= password.count(letter) <= upper_b:
            valid_count += 1
    
    return valid_count


@profiler
def part_2(lst: List[Tuple[List[str], int, int, str]]) -> int:
    """
    Validate passwords according to the updated policy where the lowerbound and upperbound
    represent indices. One of the indices must have the specified letter, but not both.

    Args:
        lst (List[Tuple[List[str], int, int, str]]): List of tuples where each tuple contains:
            - Rule, lower bound, upper bound, password
            
    Returns:
        int: The number of valid passwords according to the new policy.
    """
    valid_count = 0
    for rule, lower_b, upper_b, password in lst:
        letter = rule[1]
        # Check if only one of the specified positions contains the letter
        if (password[lower_b - 1] == letter) != (password[upper_b - 1] == letter):
            valid_count += 1
    
    return valid_count


if __name__ == "__main__":
    input_data = get_input("inputs/2_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
