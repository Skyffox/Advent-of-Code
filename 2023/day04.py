# pylint: disable=line-too-long
"""
Part 1: Find how many numbers from your card are in the winning card
Answer: 23673

Part 2: With each win we get more scratch cards, calculate how many scratch cards we end up with
Answer: 12263631
"""

from utils import profiler


def get_input(file_path: str) -> list:
    """Get the input data"""
    scratch_cards = {}
    winning_cards, your_cards = [], []
    with open(file_path, "r", encoding="utf-8") as file:
        for idx, line in enumerate(file):
            line = line.strip().split(":")[1].split("|")

            scratch_cards[idx] = 1
            winning_cards.append(line[0].strip().split(" "))
            # Edge case from the input where they put extra spaces for single digits, so filter these out.
            your_cards.append([x for x in line[1].strip().split(" ") if x != ""])

    return scratch_cards, winning_cards, your_cards


@profiler
def part_1(winning_cards: list, your_cards: list) -> int:
    """Find winning numbers and determine how much points the card is worth"""
    points = 0
    for winning_card, your_card in zip(winning_cards, your_cards):
        found_cards = len([card for card in your_card if card in winning_card])
        if found_cards > 0:
            # First number is worth 1 point, subsequent numbers multiply by 2.
            points += 2 ** (found_cards - 1)

    return points


@profiler
def part_2(scratch_cards: set, winning_cards: list, your_cards: list) -> int:
    """Update new scratch cards for cards after our current one"""
    for idx, (winning_card, your_card) in enumerate(zip(winning_cards, your_cards)):
        found_cards = len([card for card in your_card if card in winning_card])
        for i in range(idx + 1, idx + 1 + found_cards):
            if i > len(winning_cards):
                continue
            # By adding the amount for the current card instead of adding +1 we are eliminating an entire forloop.
            scratch_cards[i] += scratch_cards[idx]

    return sum(list(scratch_cards.values()))


if __name__ == "__main__":
    scratch, win, your = get_input("inputs/4_input.txt")

    print(f"Part 1: {part_1(win, your)}")
    print(f"Part 2: {part_2(scratch, win, your)}")
