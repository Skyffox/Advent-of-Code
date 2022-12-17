# Part 1: How many trees are visible from outside the grid?
# Answer: 1533

# Part 2: What is the highest scenic score possible for any tree?
# Answer: 345744

# Execution time: 0.304s

forest = []
with open("inputs/8_input.txt") as f:
    for line in f:
        line = line.strip()
        line = [int(x) for x in str(line)]
        forest.append(line)


visible_trees = len(forest) * 2 + len(forest[0]) * 2 - 4
scenic_score = 0

# Part 1
for y in range(1, len(forest) - 1):
    for x in range(1, len(forest) - 1):

        # left
        b = True
        for a in range(0, x):
            if forest[y][x] <= forest[y][a]:
                b = False
                break

        if b:
            visible_trees += 1
            continue

        # right
        b = True
        for a in range(x+1, len(forest[0])):
            if forest[y][x] <= forest[y][a]:
                b = False
                break

        if b:
            visible_trees += 1
            continue

        # top
        b = True
        for a in range(0, y):
            if forest[y][x] <= forest[a][x]:
                b = False
                break

        if b:
            visible_trees += 1
            continue

        # bottom
        b = True
        for a in range(y+1, len(forest)):
            if forest[y][x] <= forest[a][x]:
                b = False
                break

        if b:
            visible_trees += 1
            continue

print("Number of trees viewable from the edge:", visible_trees)

# Part 2
for y in range(1, len(forest) - 1):
    for x in range(1, len(forest) - 1):

        # left
        score_left = 0
        for a in range(x-1, -1, -1):
            if forest[y][x] > forest[y][a]:
                score_left += 1
            elif forest[y][x] <= forest[y][a]:
                score_left +=1
                break

        # right
        score_right = 0
        for a in range(x+1, len(forest[0])):
            if forest[y][x] > forest[y][a]:
                score_right += 1
            elif forest[y][x] <= forest[y][a]:
                score_right +=1
                break

        # top
        score_top = 0
        for a in range(y-1, -1, -1):
            if forest[y][x] > forest[a][x]:
                score_top += 1
            elif forest[y][x] <= forest[a][x]:
                score_top +=1
                break

        # bottom
        score_bottom = 0
        for a in range(y+1, len(forest)):
            if forest[y][x] > forest[a][x]:
                score_bottom += 1
            elif forest[y][x] <= forest[a][x]:
                score_bottom +=1
                break

        local_score = score_left * score_right * score_top * score_bottom
        if local_score > scenic_score:
            scenic_score = local_score

print("Highest scenic score:", scenic_score)