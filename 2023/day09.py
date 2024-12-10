# Part 1: Find the sum of extrapolated values that would come next in the series.
# Answer: 2043677056

# Part 2: Find the sum of extrapolated values that would precede the series.
# Answer: 1062

def differences(lst):
	return [lst[i+1] - lst[i] for i, _ in enumerate(lst) if i != len(lst)-1]


with open("inputs/9_input.txt") as f:
	total, total2 = 0, 0
	for line in f:
		line = list(map(int, line.strip().split(" ")))
		line_inputs = [line]

		# Part 1
		lst = differences(line)
		while lst != [0] * (len(line_inputs[-1])-1):
			line_inputs.append(lst)
			lst = differences(line_inputs[-1])

		diff = 0
		for i in range(len(line_inputs)-1, -1, -1):
			line_inputs[i].append(line_inputs[i][-1] + diff)
			diff = line_inputs[i][-1]

		# Part 2
		diff = 0
		for i in range(len(line_inputs)-1, -1, -1):
			line_inputs[i].insert(0, line_inputs[i][0] - diff)
			diff = line_inputs[i][0]
			
		total2 += line_inputs[0][0]
		total += line_inputs[0][-1]

print("Part 1", total)
print("Part 2", total2)