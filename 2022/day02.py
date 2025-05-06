# pylint: disable=line-too-long
"""
Day 2: Rock Paper Scissors

Part 1: What would your total score be if everything goes exactly according to your strategy guide?  
Answer: 11666

Part 2: Following the Elf's instructions for the second column, what would your total score be if everything goes exactly according to your strategy guide?  
Answer: 12767
"""

from typing import List
from utils import profiler


def get_input(file_path: str) -> List[List[str]]:
    """
    Parse the input file into a list of (enemy, player/outcome) moves.

    Args:
        file_path (str): Path to the input file.

    Returns:
        List[List[str]]: List of rounds, each with enemy move and your move or outcome.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip().split() for line in file]


@profiler
def part_1(rounds: List[List[str]]) -> int:
    """
    Compute the total score using the given strategy guide.
    
    The second column represents your move:  
    X = Rock, Y = Paper, Z = Scissors.  
    The score is the sum of shape score + outcome score.

    Returns:
        int: Total score.
    """
    score_map = {
        ("A", "X"): 4, ("A", "Y"): 8, ("A", "Z"): 3,
        ("B", "X"): 1, ("B", "Y"): 5, ("B", "Z"): 9,
        ("C", "X"): 7, ("C", "Y"): 2, ("C", "Z"): 6,
    }

    return sum(score_map[(enemy, player)] for enemy, player in rounds)


@profiler
def part_2(rounds: List[List[str]]) -> int:
    """
    Compute the total score using the corrected interpretation of the strategy guide.

    The second column now represents the desired outcome:  
    X = Lose, Y = Draw, Z = Win.

    Returns:
        int: Total score.
    """
    outcome_map = {
        ("A", "X"): 3, ("A", "Y"): 4, ("A", "Z"): 8,
        ("B", "X"): 1, ("B", "Y"): 5, ("B", "Z"): 9,
        ("C", "X"): 2, ("C", "Y"): 6, ("C", "Z"): 7,
    }

    return sum(outcome_map[(enemy, outcome)] for enemy, outcome in rounds)


if __name__ == "__main__":
    input_data = get_input("inputs/2_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
