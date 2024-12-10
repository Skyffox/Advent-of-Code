# Part 1: See how many times there is an increase or decrease in the data
# Answer: 1624

# Part 2: Instead compare it over a window of 3 items, in this case we only compare the first and the last of that window
# Answer: 1653


lst = []
n, n2 = 0, 0
with open("inputs/1_input.txt") as f:
    for line in f:
        lst.append(int(line.strip()))

# Part 1
for x in range(len(lst) - 1):
    if lst[x+1] > lst[x]:
        n += 1

# Part 2
for x in range(len(lst) - 3):
    if lst[x+3] > lst[x]:
        n2 += 1

print("Part 1:", n)
print("Part 1:", n2)