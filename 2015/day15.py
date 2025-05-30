# pylint: disable=line-too-long
"""
Day 15: Science for Hungry People

Part 1: Given the ingredients in your kitchen and their properties,
        what is the total score of the highest-scoring cookie you can make?
Answer: 18965440

Part 2: Given the ingredients in your kitchen and their properties,
        what is the total score of the highest-scoring cookie you can make
        with a calorie total of 500?
Answer: 15862900
"""

from typing import Dict, Tuple
import re
import itertools
from utils import profiler


def load_ingredients(file_path: str) -> Dict[str, Dict[str, int]]:
    """
    Reads the input file, parses the ingredient properties, and returns a mapping.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        Dict[str, Dict[str, int]]: Mapping from ingredient name to its properties,
            including capacity, durability, flavor, texture, and calories.
    """
    pattern = re.compile(
        r"(\w+): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)"
    )
    ingredients = {}
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            match = pattern.match(line)
            if match:
                name, capacity, durability, flavor, texture, calories = match.groups()
                ingredients[name] = {
                    "capacity": int(capacity),
                    "durability": int(durability),
                    "flavor": int(flavor),
                    "texture": int(texture),
                    "calories": int(calories),
                }
    return ingredients


def score_recipe(ingredients: Dict[str, Dict[str, int]], amounts: Tuple[int, ...]) -> int:
    """
    Calculates the total cookie score for a given distribution of ingredient amounts.

    The score is the product of the sums of each property (capacity, durability,
    flavor, texture), where any negative sums are treated as zero.

    Args:
        ingredients (Dict[str, Dict[str, int]]): Mapping of ingredient properties.
        amounts (Tuple[int, ...]): Amounts of each ingredient used (in teaspoons).

    Returns:
        int: The total score of the cookie.
    """
    properties = ["capacity", "durability", "flavor", "texture"]
    totals = {prop: 0 for prop in properties}
    for amount, (_, props) in zip(amounts, ingredients.items()):
        for prop in properties:
            totals[prop] += props[prop] * amount

    for prop in properties:
        if totals[prop] < 0:
            totals[prop] = 0

    score = 1
    for prop in properties:
        score *= totals[prop]
    return score


def calories_count(ingredients: Dict[str, Dict[str, int]], amounts: Tuple[int, ...]) -> int:
    """
    Calculates the total calories of a cookie given ingredient amounts.

    Args:
        ingredients (Dict[str, Dict[str, int]]): Mapping of ingredient properties.
        amounts (Tuple[int, ...]): Amounts of each ingredient used.

    Returns:
        int: Total calorie count of the cookie.
    """
    total_calories = 0
    for amount, (_, props) in zip(amounts, ingredients.items()):
        total_calories += props["calories"] * amount
    return total_calories


@profiler
def compute(file_path: str) -> Tuple[int, int]:
    """
    Finds the highest scoring cookie recipes for two cases:
    1. Highest total score using exactly 100 teaspoons of ingredients.
    2. Highest total score using exactly 100 teaspoons of ingredients with total calories = 500.

    Args:
        file_path (str): Path to the input file describing ingredient properties.

    Returns:
        Tuple[int, int]: 
            - Highest score without calorie restriction (Part 1).
            - Highest score with calorie restriction (Part 2).
    """
    ingredients = load_ingredients(file_path)
    n = len(ingredients)
    max_score_1, max_score_2 = 0, 0

    # Generate all combinations of ingredient amounts summing to 100 teaspoons
    for amounts in itertools.product(range(101), repeat=n):
        if sum(amounts) == 100:
            score = score_recipe(ingredients, amounts)
            if score > max_score_1:
                max_score_1 = score

            if calories_count(ingredients, amounts) == 500 and score > max_score_2:
                max_score_2 = score

    return max_score_1, max_score_2


if __name__ == "__main__":
    part1, part2 = compute("inputs/15_input.txt")

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")
