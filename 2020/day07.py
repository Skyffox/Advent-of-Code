# pylint: disable=line-too-long
"""
Day 7: Handy Haversacks

Part 1: How many bag colors can eventually contain at least one shiny gold bag? 
Answer: 272

Part 2: How many individual bags are required inside your single shiny gold bag?
Answer: 172246
"""

from typing import Dict
import re
from utils import profiler


def load_rules(file_path: str) -> Dict[str, Dict[str, int]]:
    """
    Reads the input file and parses the bag containment rules.

    Each line describes how many and what types of bags a given bag can contain.
    Returns a dictionary where each key is a bag color and the value is a dictionary
    of contained bag colors and their respective quantities.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        dict[str, dict[str, int]]: Parsed bag containment rules.
    """
    rules = {}
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            match = re.match(r"^(.*) bags contain (.*)\.$", line)
            if match:
                outer_bag = match.group(1)
                inner_bags = match.group(2)
                contained = {}

                if inner_bags != "no other bags":
                    for bag in inner_bags.split(", "):
                        count, color = re.match(r"(\d+) (.*) bag", bag).groups()
                        contained[color] = int(count)

                rules[outer_bag] = contained

    return rules


def can_contain_shiny_gold(rules: Dict[str, Dict[str, int]], bag_color: str) -> bool:
    """
    Determines if a bag can eventually contain a shiny gold bag.

    Args:
        rules (dict): A dictionary of bag containment rules.
        bag_color (str): The color of the bag to check.

    Returns:
        bool: True if the bag can eventually contain a shiny gold bag, False otherwise.
    """
    if bag_color == "shiny gold":
        return True
    for contained_bag in rules.get(bag_color, {}):
        if can_contain_shiny_gold(rules, contained_bag):
            return True
    return False


@profiler
def part_one(rules: Dict[str, Dict[str, int]]) -> int:
    """
    Counts how many different bag colors can eventually contain at least one shiny gold bag.

    Args:
        rules (dict): Bag containment rules parsed from the input.

    Returns:
        int: Number of bag colors that can eventually contain a shiny gold bag.
    """
    return sum(
        can_contain_shiny_gold(rules, bag_color) for bag_color in rules if bag_color != "shiny gold"
    )


def count_bags_inside(rules: Dict[str, Dict[str, int]], bag_color: str) -> int:
    """
    Recursively counts the total number of bags contained within the specified bag.

    Args:
        rules (dict): A dictionary of bag containment rules.
        bag_color (str): The color of the bag to count the total nested bags for.

    Returns:
        int: Total number of individual bags required inside the given bag.
    """
    return sum(
        count + count * count_bags_inside(rules, contained_bag)
        for contained_bag, count in rules.get(bag_color, {}).items()
    )


@profiler
def part_two(rules: Dict[str, Dict[str, int]]) -> int:
    """
    Calculates the total number of bags required inside a single shiny gold bag.

    Args:
        rules (dict): Bag containment rules parsed from the input.

    Returns:
        int: Total number of bags inside a shiny gold bag.
    """
    return count_bags_inside(rules, "shiny gold")


if __name__ == "__main__":
    rules_data = load_rules("inputs/7_input.txt")

    print(f"Part 1: {part_one(rules_data)}")
    print(f"Part 2: {part_two(rules_data)}")
