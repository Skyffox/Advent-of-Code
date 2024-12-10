# Part 1: Find all valid triangles, where the two smallest sides must be bigger than the largest side
# Answer: 917

# Part 2: Look at the first column of the input and determine the same thing from there
# Answer: 1649

n, n2 = 0, 0
ll, la = list(), list()
with open("inputs/3_input.txt") as f:
    for line in f:
        line = list(map(int, line.split()))
        ll.append(line[::])

        # Part 1
        line.sort()
        if line[0] + line[1] > line[2]:
            n += 1

# Part 2
for i in range (len(ll) // 3):
    for j in range(3):
        # Determine the vertical values from the first column
        ln = [ll[i*3][j], ll[i*3+1][j], ll[i*3+2][j]]
        ln.sort()
        if ln[0]+ln[1] > ln[2]:
            n2 += 1

print("Part 1:", n)
print("Part 2:", n2)