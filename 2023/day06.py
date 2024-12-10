# Part 1: Calculate in how many ways you can beat the record distance.
# Answer: 1660968

# Part 2: All time and distance inputs have been concatenated into one number, solve part 1 again for this new input.
# Answer: 26499773

from math import ceil, floor

# To solve the problem we can imagine the outcomes as a parabola. All outcomes above the x-axis are when we travelled
# further than the record distance. To calculate for which values this was the case we calculate the points of intersection
# with the x-axis with the help of the abc-formula:
# -b +- sqrt(b^2 - 4*a*c)
# -----------------------
#           2a 
# A in our case is always 1. B is equal to the time the race takes and C is the record distance.
def solve(time, distance):
	delta = (time**2 - 4*distance)**0.5
	low, high = (time - delta) / 2, (time + delta) / 2
	
	return ceil(high) - floor(low) - 1


with open("inputs/6_input.txt") as f:
	lines = []
	for line in f:
		line = line.strip().split(":")[1].split(" ")
		lines.append([int(x) for x in line if x != ""])

# Part 1
total = 1
for (time, distance) in zip(lines[0], lines[1]):
	total *= solve(time, distance)
print('The product of all instances we can beat the record distance:', total)

# Part 2
times = int("".join(map(str, lines[0])))
distances = int("".join(map(str, lines[1])))
total = solve(times, distances)
print('Instances we can beat the record for one big input:', total)