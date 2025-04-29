# pylint: disable=line-too-long
"""
Part 1: How many steps does it take node 'AAA' to reach node 'ZZZ'
Answer: 19241

Part 2: Find the amount of steps it takes for every input that ends in 'A' to end up in a node that ends in 'Z'
Answer: 9606140307013
"""

from functools import reduce
from utils import profiler


def get_input(file_path: str) -> tuple[list, tuple[int, int]]:
	"""Get the input data"""
	nodes = {}
	inp = []
	with open(file_path, "r", encoding="utf-8") as file:
		for i, line in enumerate(file):
			line = line.strip()
			if i == 0:
				inp = list(line)
			elif line != "":
				line = line.split(" = ")
				# Create a tuple of the two possible paths.
				tup = [x for x in line[1] if x.isalpha()]
				nodes.update({line[0] : ("".join(tup[:3]), "".join(tup[3:]))})

	return inp, nodes


def gcd(x, y):
	"""The Greatest Common Denominator"""
	while y:
		x, y = y, x % y
	return x


def lcm(x, y):
	"""
	The Least Common Multiple can be found by multiplying the two numbers and dividing it 
	by the Greatest Common Divisor of those two numbers.
	"""
	return int((x * y) / gcd(x, y))


def find_end(curr_pos: str, nodes: dict, inp: list) -> int:
	"""Keep looping the input and stop when we reach a node ending in 'Z'"""
	counter = 0
	while True:
		for direction in inp:
			if direction == 'L':
				curr_pos = nodes[curr_pos][0]
			else:
				curr_pos = nodes[curr_pos][1]

			counter += 1
			# Check the final letter for Z to see if we reached an ending node.
			# This wasnt really asked in part 1, but it still leads to the same answer.
			if curr_pos[-1] == 'Z':
				return counter


@profiler
def part_1(nodes: dict, inp: list) -> int:
    """Starting at AAA, follow the left/right instructions. How many steps are required to reach ZZZ"""
    return find_end('AAA', nodes, inp)


@profiler
def part_2(nodes: dict, inp: list) -> int:
	"""Simultaneously start on every node that ends with A. How many steps does it take before you're only on nodes that end with Z"""
	starting_pos = [x for x in nodes.keys() if x[-1] == 'A']
	ending_pos = [find_end(pos, nodes, inp) for pos in starting_pos]

	# Reduce applies the given function to each element in the list.
	# The LCM function is now continuously applied to the result of itself and the next element.
	return reduce(lambda x, y : lcm(x, y), ending_pos)


if __name__ == "__main__":
    input_start, node_dict = get_input("inputs/8_input.txt")

    print(f"Part 1: {part_1(node_dict, input_start)}")
    print(f"Part 2: {part_2(node_dict, input_start)}")
