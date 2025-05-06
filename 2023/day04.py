# pylint: disable=line-too-long
"""
Day 4: Scratchcards

Part 1: Find how many numbers from your card are in the winning card
Answer: 23673

Part 2: With each win we get more scratch cards, calculate how many scratch cards we end up with
Answer: 12263631
"""

from typing import List, Tuple, Dict
from utils import profiler


def get_input(file_path: str) -> Tuple[Dict[int, int], List[List[str]], List[List[str]]]:
    """
    Parse the input file to extract scratch card data.

    Args:
        file_path (str): Path to the input file.

    Returns:
        Tuple containing:
            - Dict[int, int]: Scratch cards with their counts.
            - List[List[str]]: Winning numbers per card.
            - List[List[str]]: Your numbers per card.
    """
    scratch_cards: Dict[int, int] = {}
    winning_cards: List[List[str]] = []
    your_cards: List[List[str]] = []

    with open(file_path, "r", encoding="utf-8") as file:
        for idx, line in enumerate(file):
            parts = line.strip().split(":")[1].split("|")
            scratch_cards[idx] = 1
            winning_cards.append(parts[0].strip().split())
            your_cards.append([x for x in parts[1].strip().split() if x])

    return scratch_cards, winning_cards, your_cards


@profiler
def part_1(winning_cards: List[List[str]], your_cards: List[List[str]]) -> int:
    """
    Calculate the total points based on how many winning numbers appear on each of your cards.
    First match is worth 1 point, each additional match doubles the value.

    Args:
        winning_cards (List[List[str]]): Winning numbers per card.
        your_cards (List[List[str]]): Your numbers per card.

    Returns:
        int: Total points scored across all cards.
    """
    points = 0
    for winning_card, your_card in zip(winning_cards, your_cards):
        matches = sum(1 for card in your_card if card in winning_card)
        if matches > 0:
            points += 2 ** (matches - 1)

    return points


@profiler
def part_2(scratch_cards: Dict[int, int], winning_cards: List[List[str]], your_cards: List[List[str]]) -> int:
    """
    Track the number of scratch cards obtained recursively based on wins.

    Args:
        scratch_cards (Dict[int, int]): Initial scratch cards (each starts with 1).
        winning_cards (List[List[str]]): Winning numbers per card.
        your_cards (List[List[str]]): Your numbers per card.

    Returns:
        int: Total number of scratch cards obtained.
    """
    for idx, (winning_card, your_card) in enumerate(zip(winning_cards, your_cards)):
        matches = sum(1 for card in your_card if card in winning_card)
        for i in range(idx + 1, idx + 1 + matches):
            if i >= len(winning_cards):
                break
            scratch_cards[i] += scratch_cards[idx]

    return sum(scratch_cards.values())


if __name__ == "__main__":
    scratch, win, your = get_input("inputs/4_input.txt")

    print(f"Part 1: {part_1(win, your)}")
    print(f"Part 2: {part_2(scratch, win, your)}")
