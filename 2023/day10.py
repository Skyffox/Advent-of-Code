# Part 1:
# Answer: 6757

# Part 2:
# Answer: 523


# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.
# . is ground; there is no pipe in this tile.
# S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.
def orientation(y, x):
	# print(y, x, input[y+1][x], len(input))
	if x > 0 and (y, x-1) not in visited:
		# west connecting east
		if input[y][x-1] in ("-", "L", "F") and input[y][x] in ("-", "J", "7", "S"):
			return y, x-1
	if x < len(input[0])-1 and (y, x+1) not in visited:
		# east connecting west
		if input[y][x+1] in ("-", "J", "7") and input[y][x] in ("-", "L", "F", "S"):
			return y, x+1
	if y > 0 and (y-1, x) not in visited: 
		# north connecting south
		if input[y-1][x] in ("|", "7", "F") and input[y][x] in ("|", "L", "J", "S"):
			return y-1, x
	if y < len(input) and (y+1, x) not in visited:
		# south connecting north
		if input[y+1][x] in ("|", "L", "J") and input[y][x] in ("|", "7", "F", "S"):
			return y+1, x
	
	# Search in a 3x3 grid around the coordinate for the start.
	for y_offset in range(-1, 2):
		for x_offset in range(-1, 2):
			if y + y_offset > len(input)-1 or y + y_offset < 0 or x + x_offset > len(input[0])-1 or x + x_offset < 0:
				continue
			val = input[y+y_offset][x+x_offset]
			if val == "S":
				return y+y_offset, x+x_offset
	return y, x


input = []
visited = []
pos = (0, 0)
starting_pos = (0, 0)
with open("inputs/10_input.txt") as f:
	for i, line in enumerate(f):
		line = list(line.strip())
		input.append(line)
		if 'S' in line:
			pos = (i, line.index("S"))
			starting_pos = (i, line.index("S"))
			visited.append(pos)

c = 0

while True:
	pos = orientation(pos[0], pos[1])
	c += 1
	visited.append(pos)

	if input[pos[0]][pos[1]] == "S":
		break

print(c//2)

# change S to what sign it is
# print(visited)
dir1 = tuple(map(lambda i, j: i - j, visited[0], visited[1]))
dir2 = tuple(map(lambda i, j: i - j, visited[-1], visited[-2]))
# print(dir1, dir2)
if   (dir1 == (-1, 0) or dir2 == (-1, 0)) and (dir1 == (1, 0) or dir2 == (1, 0)): start_pipe = '|'
elif (dir1 == (0, -1) or dir2 == (0, -1)) and (dir1 == (0, 1) or dir2 == (0, 1)): start_pipe = '-'
elif (dir1 == (0, 1) or dir2 == (0, 1)) and (dir1 == (1, 0) or dir2 == (1, 0)): start_pipe = 'J'
elif (dir1 == (0, -1) or dir2 == (0, -1)) and (dir1 == (1, 0) or dir2 == (1, 0)): start_pipe = 'L'
elif (dir1 == (0, 1) or dir2 == (0, 1)) and (dir1 == (-1, 0) or dir2 == (-1, 0)): start_pipe = '7'
else: start_pipe = 'F'
# print(start_pipe)
for i, row in enumerate(input):
	for j, c in enumerate(row):
		if c == "S":
			input[i][j] = start_pipe

visited = set(visited)
# print(input)
# part 2

from itertools import count

def add(ra, ca, rb, cb):
	return ra + rb, ca + cb

def find_start(grid):
	for r, row in enumerate(grid):
		for c, char in enumerate(row):
			if char == 'S':
				return r, c

def follow_pipes(grid, start_r, start_c):
	U, D, L, R = directions = ((-1, 0), (1, 0), (0, -1), (0, 1))
	possible_pipes = ('|F7', '|LJ', '-FL', '-J7')
	matches = ()

	for (dr, dc), pipes in zip(directions, possible_pipes):
		r, c = start_r + dr, start_c + dc

		if grid[r][c] in pipes:
			matches += ((dr, dc),)

	if   matches == (U, D): start_pipe = '|'
	elif matches == (L, R): start_pipe = '-'
	elif matches == (U, L): start_pipe = 'J'
	elif matches == (U, R): start_pipe = 'L'
	elif matches == (D, L): start_pipe = '7'
	else: start_pipe = 'F'

	r, c = start_r, start_c
	dr, dc = matches[0]
	seen = set([(r, c)])

	for steps in count(1):
		r, c = r + dr, c + dc
		pipe = grid[r][c]
		seen.add((r, c))

		if pipe in 'L7':
			dr, dc = dc, dr
		elif pipe in 'FJ':
			dr, dc = -dc, -dr
		elif pipe == 'S':
			break

	grid[start_r][start_c] = start_pipe
	return seen, steps

def inner_area(grid, main_loop):
	area = 0

	for r, row in enumerate(grid):
		inside = False

		for c, cell in enumerate(row):
			if (r, c) not in main_loop:
				area += inside
			else:
				inside = inside ^ (cell in '|F7')

	return area


# Open the first argument as input or use stdin if no arguments were given
fin = open("inputs/10_input.txt")

grid = list(map(list, map(str.rstrip, fin)))
main_loop, loop_len = follow_pipes(grid, *find_start(grid))
max_pipe_distance = loop_len // 2
print('Part 1:', max_pipe_distance)

# print(grid, main_loop)
# print(input, set(visited))
# print(inner_area(input, visited))
print(inner_area(input, set(visited)))
area = inner_area(grid, main_loop)
print('Part 2:', area)
