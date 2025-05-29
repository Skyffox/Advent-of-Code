# pylint: disable=line-too-long
"""
Day 14: Chocolate Charts

Part 1: What are the scores of the ten recipes immediately after the number of recipes in your puzzle input?
Answer: 8176111038

Part 2: How many recipes appear on the scoreboard to the left of the score sequence in your puzzle input?
Answer: 20225578
"""

from utils import profiler


def get_input(file_path: str) -> int:
    """
    Reads the input file and returns the puzzle input as an integer.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        int: The puzzle input number.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return int(file.read().strip())


@profiler
def part_one(recipes_after: int) -> str:
    """
    Finds the scores of ten recipes immediately after the given number of recipes.

    Args:
        recipes_after (int): Number of recipes after which to find the scores.

    Returns:
        str: The concatenated scores of the ten recipes after the given number.
    """
    recipes = [3, 7]
    elf1, elf2 = 0, 1

    while len(recipes) < recipes_after + 10:
        new_score = recipes[elf1] + recipes[elf2]
        if new_score >= 10:
            recipes.append(new_score // 10)
        recipes.append(new_score % 10)
        elf1 = (elf1 + recipes[elf1] + 1) % len(recipes)
        elf2 = (elf2 + recipes[elf2] + 1) % len(recipes)

    return ''.join(str(d) for d in recipes[recipes_after:recipes_after + 10])


@profiler
def part_two(sequence: int) -> int:
    """
    Finds how many recipes appear on the scoreboard to the left of the given sequence.

    Args:
        sequence (int): The sequence to search for.

    Returns:
        int: The number of recipes to the left of the first appearance of the sequence.
    """
    seq_str = str(sequence)
    seq_len = len(seq_str)
    recipes = [3, 7]
    elf1, elf2 = 0, 1

    while True:
        new_score = recipes[elf1] + recipes[elf2]
        if new_score >= 10:
            recipes.append(new_score // 10)
            if ''.join(str(d) for d in recipes[-seq_len:]) == seq_str:
                return len(recipes) - seq_len
        recipes.append(new_score % 10)
        if ''.join(str(d) for d in recipes[-seq_len:]) == seq_str:
            return len(recipes) - seq_len

        elf1 = (elf1 + recipes[elf1] + 1) % len(recipes)
        elf2 = (elf2 + recipes[elf2] + 1) % len(recipes)


if __name__ == "__main__":
    input_value = get_input("inputs/14_input.txt")

    print(f"Part 1: {part_one(input_value)}")
    print(f"Part 2: {part_two(input_value)}")
