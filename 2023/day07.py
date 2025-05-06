# pylint: disable=line-too-long
"""
Day 7: Camel Cards

Part 1: Find the ranks of hands in a poker game. The answer is their bid multiplied by their rank.  
Answer: 253205868

Part 2: Same as part 1, but Jacks become Jokers and can act as any card to maximize hand value.  
Answer: 253907829
"""

from enum import Enum
from typing import List, Tuple
from utils import profiler


class Hands(Enum):
    """Assign increasing numeric values to hand types (higher is better)."""
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_KIND = 3
    FULL_HOUSE = 4
    FOUR_KIND = 5
    FIVE_KIND = 6


def get_input(file_path: str) -> List[Tuple[str, str]]:
    """
    Read hand and bid data from file.

    Args:
        file_path (str): Path to input file.

    Returns:
        List[Tuple[str, str]]: List of (hand, bid) tuples.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip().split(" ") for line in file]


def find_duplicates(hand: List[int], threshold: int) -> List[int]:
    """
    Find values in the hand that appear more than `threshold` times.

    Args:
        hand (List[int]): The hand of cards (as ints).
        threshold (int): Frequency threshold.

    Returns:
        List[int]: Duplicates exceeding the threshold.
    """
    return [c for c in set(hand) if hand.count(c) > threshold]


def transform_hand(hand: List[str], is_part2: bool) -> List[int]:
    """
    Convert hand from character format to numerical format.

    Args:
        hand (List[str]): Card characters.
        is_part2 (bool): If True, treat 'J' as Joker (lowest), otherwise as Jack (11).

    Returns:
        List[int]: Numeric representation of cards.
    """
    for idx, i in enumerate(hand):
        if i == 'T':
            hand[idx] = 10
        elif i == 'J':
            hand[idx] = 0 if is_part2 else 11
        elif i == 'Q':
            hand[idx] = 11 if is_part2 else 12
        elif i == 'K':
            hand[idx] = 12 if is_part2 else 13
        elif i == 'A':
            hand[idx] = 13 if is_part2 else 14
        else:
            hand[idx] = int(i)

    return hand


def score(hand: List[int]) -> List:
    """
    Evaluate hand and return its rank and structure.

    Args:
        hand (List[int]): Numeric hand.

    Returns:
        List: [rank_value, hand]
    """
    unique = set(hand)
    if len(unique) == 5:
        return [Hands.HIGH_CARD.value, hand]
    elif len(unique) == 4:
        return [Hands.ONE_PAIR.value, hand]
    elif len(unique) == 3:
        if len(find_duplicates(hand, 1)) == 2:
            return [Hands.TWO_PAIR.value, hand]
        return [Hands.THREE_KIND.value, hand]
    elif len(unique) == 2:
        if len(find_duplicates(hand, 3)):
            return [Hands.FOUR_KIND.value, hand]
        return [Hands.FULL_HOUSE.value, hand]
    return [Hands.FIVE_KIND.value, hand]


@profiler
def part_1(inp: List[Tuple[str, str]]) -> int:
    """
    Calculate total winnings based on hand strength and rank.

    Args:
        inp (List[Tuple[str, str]]): List of (hand, bid).

    Returns:
        int: Total winnings.
    """
    hands = []
    for hand, bid in inp:
        ranked = score(transform_hand(list(hand), False))
        ranked.append(int(bid))
        hands.append(ranked)

    hands.sort(key=lambda x: (x[0], x[1]))

    return sum((i + 1) * bid for i, (_, _, bid) in enumerate(hands))


@profiler
def part_2(inp: List[Tuple[str, str]]) -> int:
    """
    Same as part_1 but 'J' is now a Joker that becomes whatever gives the highest rank.

    Args:
        inp (List[Tuple[str, str]]): List of (hand, bid).

    Returns:
        int: Total winnings.
    """
    hands = []
    for hand, bid in inp:
        if "J" not in hand:
            ranked = score(transform_hand(list(hand), True))
        else:
            joker_idxs = [i for i, c in enumerate(hand) if c == "J"]
            base_hand = transform_hand(list(hand), True)
            best_rank = [-1]
            for value in range(2, 14): # Try replacing Jokers with each possible value
                trial = base_hand[:]
                for idx in joker_idxs:
                    trial[idx] = value
                best_rank = max(score(trial), best_rank)
            ranked = [best_rank[0], base_hand]

        ranked.append(int(bid))
        hands.append(ranked)

    hands.sort(key=lambda x: (x[0], x[1]))

    return sum((i + 1) * bid for i, (_, _, bid) in enumerate(hands))


if __name__ == "__main__":
    input_data = get_input("inputs/7_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
