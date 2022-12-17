# Part 1: Find the item type that appears in both compartments of each rucksack. What is the sum of the priorities of those item types?
# Answer: 7845

# Part 2: Find the item type that corresponds to the badges of each three-Elf group. What is the sum of the priorities of those item types?
# Answer: 2790

# Execution time: 0.219s

# Split the string in two and find similar items.
def part1(lines):
    s = 0
    for i in range(0, len(lines)):
        line = list(lines[i].strip())
        first_compartment = line[:len(line)//2]
        second_compartment = line[len(line)//2:]

        for item in first_compartment:
            if item in second_compartment:
                common = item
                break

        # Account for offset
        if common.isupper():
            s += ord(common) - 38
        else:
            s += ord(common) - 96

    return s


# Find similar items, 3 lines at a time.
def part2(lines):
    s = 0
    for i in range(0, len(lines), 3):
        for item in lines[i]:
            if item in lines[i+1] and item in lines[i+2]:
                common = item
                break

        if common.isupper():
            s += ord(common) - 38
        else:
            s += ord(common) - 96
    return s


with open("inputs/3_input.txt") as f:
    s = 0
    lines = f.readlines()

print("Sum  of priorities of common items:", part1(lines))      
print("Sum of priorities of badge:", part2(lines))