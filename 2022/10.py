# Part 1: Find the signal strength during the 20th, 60th, 100th, 140th, 180th, and 220th cycles. What is the sum of these six signal strengths?
# Answer: 13920

# Part 2: Render the image given by your program. What eight capital letters appear on your CRT?
# Answer: EGLHBLFJ

# Execution time: 0.215s

initial_value = 1
counter = 1
cycles = [20, 60, 100, 140, 180, 220]
total = 0
message = []
row = []

with open("inputs/10_input.txt") as f:
    for line in f:
        line = line.strip().split()

        pos = counter % 40

        if counter in cycles:
            total += (initial_value * counter)

        if pos in range(initial_value, initial_value + 3):
            row.append("# ")
        else:
            row.append(". ")

        if pos == 0:
            message.append(row)
            row = []

        if len(line) == 2:
            counter += 1
            pos = counter % 40

            if counter in cycles:
                total += (initial_value * counter)
    
            if pos in range(initial_value, initial_value + 3):
                row.append("# ")
            else:
                row.append(". ")

            if pos == 0:
                message.append(row)
                row = []

            counter += 1
            initial_value += int(line[1])

        else:
            counter += 1

print("Total signal strength:", total)


for x in message:
    print("".join(x))