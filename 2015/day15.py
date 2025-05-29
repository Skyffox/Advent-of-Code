# pylint: disable=line-too-long
"""
Day 15: Science for Hungry People

Part 1: Given the ingredients in your kitchen and their properties, what is the total score of the highest-scoring cookie you can make?
Answer: 18965440

Part 2: Given the ingredients in your kitchen and their properties, what is the total score of the highest-scoring cookie you can make with a calorie total of 500?
Answer: 15862900
"""

from typing import List, Dict, Tuple
import re
import itertools
from utils import profiler


def get_input(file_path: str) -> List[str]:
    """
    Reads the input file and returns a list of stripped lines.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        list[str]: A list of lines with leading/trailing whitespace removed.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file]


def parse_ingredients(data: List[str]) -> Dict[str, Dict[str, int]]:
    """
    Parses ingredient properties.

    Args:
        data (List[str]): Lines describing ingredients.

    Returns:
        Dict[str, Dict[str, int]]: Mapping from ingredient name to property dict.
    """
    pattern = re.compile(
        r"(\w+): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)"
    )
    ingredients = {}
    for line in data:
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
    Calculates the total score for a recipe given ingredient amounts.

    Args:
        ingredients (Dict[str, Dict[str, int]]): Ingredient properties.
        amounts (Tuple[int, ...]): Amounts for each ingredient.

    Returns:
        int: Total score (product of summed properties, min 0).
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
    Calculates total calories for a recipe.

    Args:
        ingredients (Dict[str, Dict[str, int]]): Ingredient properties.
        amounts (Tuple[int, ...]): Amounts for each ingredient.

    Returns:
        int: Total calories.
    """
    total_calories = 0
    for amount, (_, props) in zip(amounts, ingredients.items()):
        total_calories += props["calories"] * amount
    return total_calories


@profiler
def compute(data_input: List[str]) -> Tuple[int, int]:
    """
    Finds the highest scoring cookie (total teaspoons = 100).

    Args:
        data_input (List[str]): Input lines describing ingredients.

    Returns:
        int: Highest total score.
    """
    ingredients = parse_ingredients(data_input)
    n = len(ingredients)
    max_score_1, max_score_2 = 0, 0

    # Generate all combinations of amounts summing to 100
    for amounts in itertools.product(range(101), repeat=n):
        if sum(amounts) == 100:
            score = score_recipe(ingredients, amounts)
            if score > max_score_1:
                max_score_1 = score

            if calories_count(ingredients, amounts) == 500 and score > max_score_2:
                max_score_2 = score

    return max_score_1, max_score_2


if __name__ == "__main__":
    input_data = get_input("inputs/15_input.txt")

    part1, part2 = compute(input_data)

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")
