# Part 1: Find all the trees we encounter if go down 1 and 3 to the right
# Answer: 278

# Part 2: Do the same but for different steps to the right and bottom
# Answer: 9709761600


def slope(grid, dx, dy):
    n, x, y = 0, 0, 0

    while y < len(grid) - 1:
        x += dx
        # We can keep propagating to the right, so we need to "reset" the grid
        if x >= len(grid[0]):
            x %= len(grid[0])

        y += dy
        if grid[y][x] == "#":
            n += 1

    return n


grid = []
n, n2 = 0, 1
with open("inputs/3_input.txt") as f:
    for line in f:
        grid.append(line.strip())

# Part 1
n = slope(grid, 3, 1)

# Part 2
n2 *= slope(grid, 1, 1)
n2 *= slope(grid, 3, 1)
n2 *= slope(grid, 5, 1)
n2 *= slope(grid, 7, 1)
n2 *= slope(grid, 1, 2)


print("Part 1:", n)
print("Part 2:", n2)