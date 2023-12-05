# Part 1: Get the numeric calibration values from the input.
# Answer: 54081

# Part 2: Get the calibration values like in part 1 whilst converting digits in their alfabetic form to their numeric form.
# Answer: 54649

digits = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

with open("inputs/1_input.txt") as f:
    total_part1 = 0  
    total_part2 = 0
    for line in f:
        line = line.strip()

        # Part 1
        numbers = [str(x) for x in line if x.isnumeric()]
        if (numbers != []):
            total_part1 += int("".join([numbers[0], numbers[-1]]))

        # Part 2
        while (True):
            # Find all indices where we find a number not in numeric notation.
            indices = [(line.find(number), index + 1) for index, number in enumerate(digits) if line.find(number) != -1]
            if (indices != []):
                line = list(line)
                # Replace the first index of the number with the numeric equivalent. Cast to list and back so we can mutate.
                for index in indices:
                    line[index[0]] = str(index[1])
                line = "".join(line)
            else:
                break

        # Add the first and last numeric value of the input string.
        numbers = [str(x) for x in line if x.isnumeric()]
        if (numbers != []):
            total_part2 += int("".join([numbers[0], numbers[-1]]))
            
print("Total of joined first and last value of each line in input:", total_part1)
print("Total of joined first and last value with numeric and non numeric input:", total_part2)
