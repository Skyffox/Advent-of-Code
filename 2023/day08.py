# Part 1: How many steps does it take node 'AAA' to reach node 'ZZZ'.
# Answer: 19241

# Part 2: Find the amount of steps it takes for every input that ends in 'A' to end up in a node that ends in 'Z'.
# Answer: 9606140307013

from functools import reduce


# Keep looping the input and stop when we reach a node ending in 'Z'.
def find_end(curr_pos):
	counter = 0
	while True:
		for direction in input:
			if direction == 'L':
				curr_pos = nodes[curr_pos][0]
			else:
				curr_pos = nodes[curr_pos][1]

			counter += 1
			# Check the final letter for Z to see if we reached an ending node. 
			# This wasnt really asked in part 1, but it still leads to the same answer.
			if curr_pos[-1] == 'Z':
				return counter

# The Greatest Common Denominator
def GCD(x, y):
	while y:
		x, y = y, x % y
	return x

# The Least Common Multiple can be found by multiplying the two numbers and dividing it by the Greatest Common Divisor of those two numbers.
def LCM(x, y):   
	return int((x * y) / GCD(x, y))


nodes = {}
with open("inputs/8_input.txt") as f:
	for i, line in enumerate(f):
		line = line.strip()
		if i == 0:
			input = list(line)
		elif line != "":
			line = line.split(" = ")
			# Create a tuple of the two possible paths.
			tup = [x for x in line[1] if x.isalpha()]
			nodes.update({line[0] : ("".join(tup[:3]), "".join(tup[3:]))})

# Part 1
print("Steps it took to find ZZZ:", find_end('AAA'))

# Part 2
starting_pos = [x for x in nodes.keys() if x[-1] == 'A']
ending_pos = [find_end(pos) for pos in starting_pos]

# Reduce applies the given function to each element in the list. 
# The LCM function is now continuously applied to the result of itself and the next element.
print("Steps it took for all inputs ending in 'A' to end up in a node ending in 'Z':", reduce(lambda x, y : LCM(x, y), ending_pos))