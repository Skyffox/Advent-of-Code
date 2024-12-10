# Part 1: Find out what our position is after following the commands
# Answer: 2073315

# Part 2: Now there is another factor that influences our course
# Answer: 1840311528


x, y = 0, 0
position, depth, aim = 0, 0, 0
with open("inputs/2_input.txt") as f:
    for line in f:
        move = line.strip().split(" ")
        units = int(move[1])
        
        # Part 1
        if move[0] == "forward":
            x += units
        elif move[0] == "down":
            y += units
        elif move[0] == "up":
            y -= units

        # Part 2
        if move[0] == "forward":
            position += units
            depth += aim * units
        elif move[0] == "down":
            aim += units
        elif move[0] == "up":
            aim -= units


print("Part 1:", x * y)
print("Part 2:", position * depth)