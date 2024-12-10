# Part 1: How many units of sand come to rest before sand starts flowing into the abyss below?
# Answer: 728

# Part 2: Using your scan, simulate the falling sand until the source of the sand becomes blocked. How many units of sand come to rest?
# Answer: 27623

sand_start = [500, 0]
canvas = []
walls = []

with open("inputs/14_input.txt") as f:
    for line in f:
        line = line.strip().split(" -> ")
        line = [x.split(",") for x in line]
        line = [list(map(int, y)) for y in line]

        for x in range(len(line)):
            walls.append(line[x])
            if x == len(line) - 1:
                break

            # Find all the walls
            if line[x][0] != line[x+1][0]:
                diff = abs(line[x][0] - line[x+1][0])
                if line[x][0] > line[x+1][0]:
                    for d in range(1, diff):
                        walls.append([line[x][0] - d, line[x][1]])
                else:
                    for d in range(1, diff):
                        walls.append([line[x][0] + d, line[x][1]])
            else:
                diff = abs(line[x][1] - line[x+1][1])
                if line[x][1] > line[x+1][1]:
                    for d in range(1, diff):
                        walls.append([line[x][0], line[x][1] - d])
                else:
                    for d in range(1, diff):
                        walls.append([line[x][0], line[x][1] + d])


min_x = min([x[0] for x in walls])
max_x = max([x[0] for x in walls])
max_y = max([x[1] for x in walls])

# ENABLE FOR PART 2
min_x -= 200
max_x += 200

# DRAW: rock as #, air as ., and the source of the sand as +
for y in range(max_y + 1):
    canvas_line = []
    for pos_x in range(min_x, max_x + 1):
        if [pos_x, y] in walls:
            canvas_line.append("# ")
        elif [pos_x, y] == sand_start:
            canvas_line.append("+ ")
        else:
            canvas_line.append(". ")
    canvas.append(canvas_line)


def sand_propagation():
    y = sand_start[1]
    x = sand_start[0] - min_x

    while True:
        if y > len(canvas)-2 or x < 0 or x > len(canvas[0]) - 1:
            return True

        if canvas[y+1][x] == ". ":
            y += 1
        elif canvas[y+1][x-1] == ". ":
            x -= 1
            y += 1
        elif canvas[y+1][x+1] == ". ":
            x += 1
            y += 1
        else:
            if canvas[y][x] == "+ ":
                return True
            canvas[y][x] = "* "
            break


# PART 1
overflow_count = 0
while True:
    overflow_count += 1
    if sand_propagation():
        print("Sand particles before overflowing:", overflow_count - 1)
        break

# PART 2
overflow_count = 0
canvas.append([". " for _ in range(min_x, max_x + 1)])
canvas.append(["# " for _ in range(min_x, max_x + 1)])

while True:
    overflow_count += 1
    if sand_propagation():
        print("Sand particles before overflowing, with floor:", overflow_count) # We are not counting the last action
        break

# PRINT THE PYRAMID
# for sub in canvas:
#     print(" ".join(sub))