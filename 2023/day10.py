# pylint: disable=line-too-long
"""
Part 1: How many steps along the loop does it take to get from the starting position to the point farthest from the starting position?
Answer: 6757

Part 2: How many tiles are enclosed by the loop?
Answer: 523
"""

from utils import profiler


def get_input(file_path: str) -> list:
	"""Get the input data"""
	lst = []
	starting_pos = (0, 0)
	with open(file_path, "r", encoding="utf-8") as file:
		for i, line in enumerate(file):
			line = list(line.strip())
			lst.append(line)
			if 'S' in line:
				starting_pos = (i, line.index("S"))

	return lst, starting_pos


@profiler
def part_1(grid, start_r, start_c):
	"""Find the giant loop, which we do by taking steps and stop when we end up at the start again."""
	directions = ((-1, 0), (1, 0), (0, -1), (0, 1))
	possible_pipes = ('|F7', '|LJ', '-FL', '-J7')
	steps = 0

	# Find the starting position
	for (delta_r, delta_c), pipes in zip(directions, possible_pipes):
		r, c = start_r + delta_r, start_c + delta_c

		if grid[r][c] in pipes:
			dr, dc = delta_r, delta_c
			r, c = start_r, start_c
			break

	seen = set([(r, c)])
	# Take a step and determine what direction we are going next
	while True:
		r, c = r + dr, c + dc
		pipe = grid[r][c]
		seen.add((r, c))
		steps += 1

		if pipe in 'L7':
			dr, dc = dc, dr
		elif pipe in 'FJ':
			dr, dc = -dc, -dr
		elif pipe == 'S':
			break

	return seen, steps


@profiler
def part_2(grid, main_loop):
	"""Run alongside the main loop that we found in part 1 and based on the pipes, we know whether we are still inside"""
	area = 0

	for r, row in enumerate(grid):
		inside = False
		for c, cell in enumerate(row):
			if (r, c) not in main_loop:
				area += inside
			else:
				inside = inside ^ (cell in '|F7')

	return area


if __name__ == "__main__":
	input_data, start = get_input("inputs/10_input.txt")

	loop, loop_len = part_1(input_data, *start)
	
	print(f"Part 1: {loop_len // 2}")
	print(f"Part 2: {part_2(input_data, loop)}")
