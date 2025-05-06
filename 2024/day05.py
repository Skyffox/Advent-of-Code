# pylint: disable=line-too-long
"""
Day 5: Print Queue

Part 1: See if the given pages from the input are in the right order
Answer: 6498

Part 2: Fix the incorrectly ordered updates by applying the ordering rules
Answer: 5017
"""

from typing import List, Tuple
from utils import profiler


def get_input(file_path: str) -> Tuple[List[List[int]], List[Tuple[int, int]]]:
    """
    Parse the input file into pages and rules.
    Each page is a list of integers (comma-separated).
    Each rule is a tuple of two integers separated by '|'.

    Args:
        file_path (str): Path to the input file.

    Returns:
        Tuple[List[List[int]], List[Tuple[int, int]]]: A tuple of pages and rules.
    """
    pages: List[List[int]] = []
    rules: List[Tuple[int, int]] = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if "|" in line:
                left, right = map(int, line.split("|"))
                rules.append((left, right))
            elif line:
                pages.append(list(map(int, line.split(","))))
    return pages, rules


def check_correctness(page: List[int], rules: List[Tuple[int, int]]) -> bool:
    """
    Check if a page is correctly ordered according to the rules.

    A page is incorrect if a rule's 'after' value appears before the 'before' value.

    Args:
        page (List[int]): The list of numbers in the page.
        rules (List[Tuple[int, int]]): List of (before, after) rules.

    Returns:
        bool: True if the page is in the correct order, False otherwise.
    """
    for idx, page_number in enumerate(page):
        for before, after in rules:
            # Check the first number of each rule. If the second number in the rule
            # comes before the first number in the page, the order is incorrect.
            if before == page_number and after in page[:idx]:
                return False
    return True


@profiler
def part_1(pages: List[List[int]], rules: List[Tuple[int, int]]) -> int:
    """
    Return the sum of medians of correctly ordered pages.

    Args:
        pages (List[List[int]]): The pages to check.
        rules (List[Tuple[int, int]]): The ordering rules.

    Returns:
        int: The sum of the middle element of each correctly ordered page.
    """
    return sum(page[len(page) // 2] for page in pages if check_correctness(page, rules))


@profiler
def part_2(pages: List[List[int]], rules: List[Tuple[int, int]]) -> int:
    """
    Attempt to fix incorrect pages using the rules, and return the sum of the median values.

    A page is "fixed" by counting how many dependencies (rules) each item has
    and sorting by that count to infer the correct order.

    Args:
        pages (List[List[int]]): The pages to fix.
        rules (List[Tuple[int, int]]): The ordering rules.

    Returns:
        int: The sum of the middle elements of the fixed pages.
    """
    total = 0
    for page in pages:
        if not check_correctness(page, rules):
            counts = []
            for item in page:
                # Count how many rules refer to 'item' needing to appear after others in this page
                dependency_count = sum(1 for before, after in rules if before == item and after in page)
                counts.append((item, dependency_count))

            # Sort by dependency count descending to simulate proper ordering
            counts.sort(key=lambda x: x[1], reverse=True)

            # Add the middle element of the "fixed" page
            total += counts[len(page) // 2][0]
    return total


if __name__ == "__main__":
    input_data, ordering_rules = get_input("inputs/5_input.txt")

    print(f"Part 1: {part_1(input_data, ordering_rules)}")
    print(f"Part 2: {part_2(input_data, ordering_rules)}")
