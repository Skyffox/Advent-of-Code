# Part 1: Calculate the eventual frequency we end up on
# Answer: 505

# Part 2: Find the frequency we land on twice for the first time
# Answer: 72330 (takes a bit)

lst = []
with open("inputs/1_input.txt") as f:
    for line in f:
        lst.append(line.strip())

inp = [int(x) for x in lst]

# Part 1
frequency = sum(inp)

# Part 2
terminated = False
seen_frequencies = [0]

while not terminated:
    for f in inp:
        curr_freq = seen_frequencies[-1] + f
        if curr_freq in seen_frequencies:
            terminated = True
            break

        seen_frequencies.append(curr_freq)

print("Part 1:", frequency)
print("Part 2:", curr_freq)