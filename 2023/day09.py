# pylint: disable=line-too-long
"""
Part 1: Find the sum of extrapolated values that would come next in the series
Answer: 2043677056

Part 2: Find the sum of extrapolated values that would precede the series
Answer: 1062
"""

from utils import profiler


def get_input(file_path: str) -> list:
	"""Get the input data"""
	with open(file_path, "r", encoding="utf-8") as file:
		return [list(map(int, line.strip().split(" "))) for line in file]


def differences(lst):
	"""Make a list of the differences between subsequent indices"""
	return [lst[i+1] - lst[i] for i, _ in enumerate(lst) if i != len(lst) - 1]


@profiler
def compute(lst: list) -> int:
	"""Extrapolate which values came before and after the original sequence based on the differences"""
	total_part1, total_part2 = 0, 0
	for line in lst:
		line_inputs = [line]

		# Keep comparing differences until all differences are 0
		lst = differences(line)
		while lst != [0] * (len(line_inputs[-1]) - 1):
			line_inputs.append(lst)
			lst = differences(line_inputs[-1])

		# Figure out the next value in the original sequence by calculating back through the last difference of each row
		diff = 0
		for i in range(len(line_inputs) - 1, -1, -1):
			line_inputs[i].append(line_inputs[i][-1] + diff)
			diff = line_inputs[i][-1]

		# Do the same as the code block above but now calculate what value came before in the sequence
		diff = 0
		for i in range(len(line_inputs) - 1, -1, -1):
			line_inputs[i].insert(0, line_inputs[i][0] - diff)
			diff = line_inputs[i][0]

		# Add the values that came before/after to the total
		total_part1 += line_inputs[0][-1]
		total_part2 += line_inputs[0][0]

	return total_part1, total_part2


if __name__ == "__main__":
	input_data = get_input("inputs/9_input.txt")

	ans_part1, ans_part2 = compute(input_data)

	print(f"Part 1: {ans_part1}")
	print(f"Part 2: {ans_part2}")
