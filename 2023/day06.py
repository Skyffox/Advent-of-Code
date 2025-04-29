# pylint: disable=line-too-long
"""
Part 1: Calculate in how many ways you can beat the record distance
Answer: 1660968

Part 2: All time and distance inputs have been concatenated into one number, solve part 1 again for this new input
Answer: 26499773
"""

from math import ceil, floor, prod
from utils import profiler


def get_input(file_path: str) -> list:
	"""Get the input data"""
	lines = []
	with open(file_path, "r", encoding="utf-8") as file:
		for line in file:
			line = line.strip().split(":")[1].split(" ")
			lines.append([int(x) for x in line if x != ""])

	return lines

# To solve the problem we can imagine the outcomes as a parabola. All outcomes above the x-axis are when we travelled
# further than the record distance. To calculate for which values this was the case we calculate the points of intersection
# with the x-axis with the help of the abc-formula:
# -b +- sqrt(b^2 - 4*a*c)
# -----------------------
#           2a
# A in our case is always 1. B is equal to the time the race takes and C is the record distance.
def solve(time, distance):
	delta = (time**2 - 4 * distance)**0.5
	low, high = (time - delta) / 2, (time + delta) / 2

	return ceil(high) - floor(low) - 1


@profiler
def part_1(lst: list) -> int:
	"""
	The distance is the record that was done in that time, we calculate how much further we can get during that 
	same time, for each reach we get an amount of ways we can beat the record. Our answer the product of all these numbers.
	"""
	return prod(solve(time, distance) for time, distance in zip(lst[0], lst[1]))


@profiler
def part_2(lst: list) -> int:
	"""Same as part 1 but there is only one race and we had to combine all numbers together"""
	return solve(int("".join(map(str, lst[0]))), int("".join(map(str, lst[1]))))


if __name__ == "__main__":
    input_data = get_input("inputs/6_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
