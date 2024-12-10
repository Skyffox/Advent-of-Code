# Part 1: Find the item type that appears in both compartments of each rucksack. What is the sum of the priorities of those item types?
# Answer: 7845

# Part 2: Find the item type that corresponds to the badges of each three-Elf group. What is the sum of the priorities of those item types?
# Answer: 2790


lst = []
with open("inputs/3_input.txt") as f:
    for line in f:
        lst.append(line.strip())