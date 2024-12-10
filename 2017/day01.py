# Part 1: Find the sum of all digits that match the next digit in the list and the list is circular
# Answer: 1253

# Part 2: Do the same but now check not the next digit but the digit halfway further up the list
# Answer: 1278

with open("inputs/1_input.txt") as f:
    for line in f:
        inp = list(line.strip())
        inp = [int(x) for x in inp]

        # Part 1
        # Check an item in the list against the next one
        matches = sum([i for i, j in zip(inp, inp[1:]) if i == j])
        # Above loop does not match the first to the last, since the list is circular
        matches += inp[0] if inp[0] == inp[-1] else 0

        # Part 2
        matches_part2 = sum([2 * i for i, j in zip(inp, inp[len(inp)//2:]) if i == j])

print("Part 1:", matches)
print("Part 2:", matches_part2)