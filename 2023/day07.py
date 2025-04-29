# pylint: disable=line-too-long
"""
Part 1: Find the ranks of hands in a poker game. The answer is their bid multiplied by their rank
Answer: 253205868

Part 2: Same as part 1, but the Jack has become a Joker which transform into a card that makes the hand have the highest value possible
Answer: 253907829
"""

from enum import Enum
from utils import profiler


class Hands(Enum):
    """Assign values to each hand, higher is better"""
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_KIND = 3
    FULL_HOUSE = 4
    FOUR_KIND = 5
    FIVE_KIND = 6


def get_input(file_path: str) -> list:
    """Get the input data"""
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip().split(" ") for line in file]


def find_duplicates(hand, t):
    """Find any duplicates in a list with certain appearance rate"""
    return [c for c in set(hand) if hand.count(c) > t]


def transform_hand(hand: list, is_part2: bool) -> list:
    """Transform special cards to a normal or adjusted value"""
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


def score(hand: list) -> list:
    """Determine the rank of the hand"""
    rank = 0

    # High card.
    if len(set(hand)) == len(hand):
        rank = [Hands.HIGH_CARD.value, hand]

    # One pair.
    if len(set(hand)) == 4:
        rank = [Hands.ONE_PAIR.value, hand]

    if len(set(hand)) == 3:
        # Two pair.
        if len(find_duplicates(hand, 1)) == 2:
            rank = [Hands.TWO_PAIR.value, hand]
        # Three of a kind.
        else:
            rank = [Hands.THREE_KIND.value, hand]

    if len(set(hand)) == 2:
        # Four of a kind.
        if len(find_duplicates(hand, 3)):
            rank = [Hands.FOUR_KIND.value, hand]
        # Full house.
        else:
            rank = [Hands.FULL_HOUSE.value, hand]

    # Five of a kind.
    if len(set(hand)) == 1:
        rank = [Hands.FIVE_KIND.value, hand]

    return rank


@profiler
def part_1(inp: list) -> int:
    """Determine the total winnings from calculating the ranks of hands we have been dealt"""
    lst = []
    total = 0

    # Group the value of the hand, the actual hand and the bid together
    for hand, bid in inp:
        rank = score(transform_hand(list(hand), False))
        rank.append(int(bid))
        lst.append(rank)

    # Sort best ranks on the best value hand
    sorted_ranks = sorted(lst, key=lambda x: (x[0], x[1]))
    for idx, (_, _, bid) in enumerate(sorted_ranks):
        # The total winnings of a set of hands are calculated by adding up the result of multiplying each hand's bid with its rank
        total += (idx + 1) * bid

    return total


@profiler
def part_2(inp: list) -> int:
    """t"""
    lst = []
    total = 0

    for hand, bid in inp:
        # Find indices where we have a J and replace this with something that is higher.
        if "J" not in hand:
            rank = score(transform_hand(list(hand), True))
        else:
            joker_indices = [i for i, c in enumerate(hand) if c == "J"]
            hand = transform_hand(list(hand), True)
            best = [-1]
            # Exhaustive search for highest score.
            for x in range(2, 14):
                new_hand = hand[:]
                # Dont need to think of combinations of values for J to find the highest score.
                for idx in joker_indices:
                    new_hand[idx] = x

                best = max(score(new_hand), best)
            rank = [best[0], hand]

        rank.append(int(bid))
        lst.append(rank)

    # Sort best ranks on the best value hand
    sorted_ranks = sorted(lst, key=lambda x: (x[0], x[1]))
    for idx, (_, _, bid) in enumerate(sorted_ranks):
        total += (idx + 1) * bid

    return total


if __name__ == "__main__":
    input_data = get_input("inputs/7_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
