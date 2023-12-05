# Part 1: Find how many numbers from your card are in the winning card.
# Answer: 23673

# Part 2: With each win we get more scratch cards, calculate how many scratch cards we end up with.
# Answer: 12263631


# We need to establish a data source before we loop over our input.
with open("inputs/4_input.txt") as lines:
    scratch = {}
    lines_count = len(lines.readlines())
    for i in range(0, lines_count):
        # The starting amount we have of each scratch card.
        scratch[i] = 1

with open("inputs/4_input.txt") as f:
    points = 0

    for idx, line in enumerate(f):
        # Take the cards from the input.
        line = line.strip().split(":")[1].split("|")
        
        winning_cards = line[0].strip().split(" ")
        your_cards = line[1].strip().split(" ")
        # Edge case from the input where the put extra spaces for single digits, so filter these out.
        your_cards = [x for x in your_cards if x != ""]
        
        # Part 1 - Find winning numbers.
        found_cards = len([card for card in your_cards if card in winning_cards])
        if found_cards > 0:
            # First number is worth 1 point, subsequent numbers multiply by 2.
            points += 2 ** (found_cards - 1)

        # Part 2 - Update new scratch cards for cards after our current one.
        for i in range(idx + 1, idx + 1 + found_cards):
            if i > lines_count:
                continue
            # By adding the amount for the current card instead of adding +1 we are eliminating an entire forloop.
            scratch[i] += scratch[idx]


print("Amount of points we get from winning numbers in our scratch cards:", points)
print("Amount of scratch cards we end up with if we get more from winning:", sum([x for x in scratch.values()]))