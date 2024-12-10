# Part 1: Find two numbers in the input that add together to 2020
# Answer: 445536

# Part 2: Now do the same but for 3 numbers
# Answer: 138688160

lst = []
with open("inputs/1_input.txt") as f:
    for line in f:
        lst.append(int(line.strip()))

# Part 1
n = 0
for idx, x in enumerate(lst):
    for y in lst[idx+1:]:
        if x + y == 2020:
            n = x * y

# Part 2
n2 = 0
for idx, x in enumerate(lst):
    for idx2, y in enumerate(lst[idx+1:]):
        for z in lst[idx+1:]:
            if x + y + z == 2020:
                n2 = x * y * z


print("Part 1:", n)
print("Part 2:", n2)