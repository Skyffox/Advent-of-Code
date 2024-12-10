# Part 1: Find the differences between the biggest and smallest number of each row
# Answer: 47136

# Part 2: See what numbers create an integer when dividing in that same row
# Answer: 250


checksum = 0
res = 0
with open("inputs/2_input.txt") as f:
    for line in f:
        inp = line.strip().split("\t")
        inp = [int(x) for x in inp]

        # Part 1
        checksum += max(inp) - min(inp)

        # Part 2
        # Sort first so the big number is divided by the small number
        inp.sort(reverse=True)
        for idx, i in enumerate(inp):
            for j in inp[idx+1:]:
                if (i / j).is_integer():
                    res += i/j

print("Part 1:", checksum)
print("Part 2:", res)