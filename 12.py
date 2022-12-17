# CLEARED 0 STARS

# Read all lines, get height and width and start and end positions
with open('small_puzzle.txt') as f:
    lines = [x.strip() for x in f.readlines()]
    width_map = len(lines)
    height_map = len(list(lines[0]))
    map = []

    for i, line in enumerate(lines):
        lst = list(line.strip())
        map.append(line)

        for j, pos in enumerate(lst):
            if pos == "S":
                start_pos = [i, j]
            if pos == "E":
                end_pos = [i, j]

# map = map[::-1]
pos = start_pos
pos_val = '`'
steps = 0
left = "NaN"
right = "NaN"
top = "NaN"
bottom = "NaN" 
print(pos)

while pos != "E":
    if pos[0] > 0:
        left = map[pos[0]][pos[1] - 1]
    if pos[0] < width_map:    
        right = map[pos[0]][pos[1] + 1]
    if pos[1] > 0:
        top = map[pos[0] + 1][pos[1]]
    if pos[1] < height_map:
        bottom = map[pos[0] - 1][pos[1]]
    
    print(pos, bottom, left, right, top, pos_val)
    if bottom != "NaN":
        if ord(bottom) - ord(pos_val) < 2:
            pos_val = bottom
            pos = [pos[0] + 1, pos[1]]
            continue
    # if right != "NaN":
    #     if map[ord(right)] - map[ord(pos)] < 2:
    #         pos = right
    #         continue
    # if top != "NaN":
    #     if map[ord(top)] - map[ord(pos)] < 2:
    #         pos = top
    #         continue
    # if left != "NaN":
    #     if map[ord(left)] - map[ord(pos)] < 2:
    #         pos = left
    #         continue

    print(pos, left, right, top, bottom)
    break