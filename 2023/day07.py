# Part 1: Find the ranks of hands in a poker game. The answer is their bid multiplied by their rank.
# Answer: 253205868

# Part 2: Same as part 1, but the Jack has become a Joker which transform into a card that makes the hand have the highest value possible.
# Answer: 253907829

from collections import defaultdict
from enum import Enum

# Assign values to each hand, higher is better.
class Hands(Enum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_KIND = 3
    FULL_HOUSE = 4
    FOUR_KIND = 5
    FIVE_KIND = 6

# Find any duplicates in a list with certain appearance rate.
def find_duplicates(hand, t):
    card_dict = defaultdict(int)
    for i in hand:
        card_dict[i] += 1

    return [v for v in card_dict if card_dict[v] > t]

# Transform special cards to a normal value.
def transform_hand(hand, normal):
    for idx, i in enumerate(hand):
		# Part 1
        if normal:
            if i == 'T': hand[idx] = 10
            elif i == 'J': hand[idx] = 11
            elif i == 'Q': hand[idx] = 12
            elif i == 'K': hand[idx] = 13
            elif i == 'A': hand[idx] = 14
            else: hand[idx] = int(i)
        # Part 2
        else:
            if i == 'T': hand[idx] = 10
            elif i == 'J': hand[idx] = 0
            elif i == 'Q': hand[idx] = 11
            elif i == 'K': hand[idx] = 12
            elif i == 'A': hand[idx] = 13
            else: hand[idx] = int(i)

    return hand

def score(hand):
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


with open("inputs/7_input.txt") as f:
    ranks_part1 = []
    ranks_part2 = []
    for line in f:
        line = line.strip().split(" ")
        hand = line[0]
        bid = line[1]
        
        # Part 1 - Keep normal scoring.
        rank = score(transform_hand([x for x in hand], True))
        rank.append(int(bid))
        ranks_part1.append(rank)

        # Part 2 - Find indices where we have a J and replace this with something that is higher.
        if "J" not in hand:
            rank = score(transform_hand([x for x in hand], False))
        else:
            joker_indices = [i for i, c in enumerate(hand) if c == "J"]
            hand = transform_hand([x for x in hand], False)
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
        ranks_part2.append(rank)
    
# Part 1
sorted_ranks = sorted(ranks_part1, key=lambda x: (x[0], x[1]))
total = 0
for idx, (_, _, bid) in enumerate(sorted_ranks):
    total += (idx+1) * bid
print("Total of bids after normal rules:", total)

# Part 2
sorted_ranks = sorted(ranks_part2, key=lambda x: (x[0], x[1]))
total = 0
for idx, (_, _, bid) in enumerate(sorted_ranks):
    total += (idx+1) * bid
print("Total of bids after adjusted rules:", total)