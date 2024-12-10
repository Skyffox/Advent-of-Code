# Part 1: See how many blocks we are away from the start after following instructions
# Answer: 252

# Part 2: Check for a path and see where we have been before
# Answer: 143

pos = [0, 0]
visited = [[0, 0]]
orientation = "N"

def move(orientation, direction, distance):
    # Some cases we move in the same direction, we need a for loop to keep track of all 
    # the positions in the grid we have been to.
    if (orientation == "N" and direction == "L") or (orientation == "S" and direction == "R"):
        orientation = "W"
        for x in range(pos[0] - 1, pos[0] - distance - 1, -1):
            pos[0] -= 1
            visited.append([x, pos[1]]) 
    
    elif (orientation == "N" and direction == "R") or (orientation == "S" and direction == "L"):
        orientation = "E"
        for x in range(pos[0] + 1, pos[0] + distance + 1):
            pos[0] += 1
            visited.append([x, pos[1]]) 
    
    elif (orientation == "W" and direction == "L") or (orientation == "E" and direction == "R"):
        orientation = "S"
        for y in range(pos[1] - 1, pos[1] - distance - 1, -1):
            pos[1] -= 1
            visited.append([pos[0], y]) 

    elif (orientation == "E" and direction == "L") or (orientation == "W" and direction == "R"):
        orientation = "N"
        for y in range(pos[1] + 1, pos[1] + distance + 1):
            pos[1] += 1
            visited.append([pos[0], y]) 

    return orientation


with open("inputs/1_input.txt") as f:
    for line in f:
        instructions = line.strip().split(", ")
        
# Part 1
for instruction in instructions:
    instruction = [c for c in instruction]
    orientation = move(orientation, instruction[0], int("".join(instruction[1:])))

# Part 2
for idx, v in enumerate(visited):
    # See what position occurs in the rest of the list
    if v in visited[idx+1:]:
        first_place = v
        break


print("Part 1:", abs(pos[0]) + abs(pos[1]))
print("Part 2:", abs(first_place[0]) + abs(first_place[1]))