# Part 1: Find all the squares in a grid that have overlap between two or more claim ids
# Answer: 118322

# Part 2: Find the claim id that has no overlap
# Answer: 1178

grid = {}
claims = []
with open("inputs/3_input.txt") as f:
    for line in f:
        inp = line.strip().split()

        # Part 1
        claim_id = inp[0].split("#")[1]
        width_start = int(inp[2].split(",")[0])
        height_start = int(inp[2].split(",")[1].split(":")[0])
        width = int(inp[3].split("x")[0])
        height = int(inp[3].split("x")[1])

        claims.append([width_start, height_start, width, height, claim_id])

        # Add all squares to a grid and update ones we have already seen
        for x in range(width_start, width_start + width):
            for y in range(height_start, height_start + height):
                if not (x, y) in grid:
                    grid[(x, y)] = 1
                else:
                    grid[(x, y)] += 1

# Part 2
for c in claims:
    overlap = False
    # Iterate over all claims again and see where there is no overlap
    for x in range(c[0], c[0] + c[2]):
        for y in range(c[1], c[1] + c[3]):
            if grid[(x, y)] > 1:
                overlap = True
    if not overlap:
        break

print("Part 1:", sum([1 for val in grid.values() if val > 1]))
print("Part 1:", c[4])