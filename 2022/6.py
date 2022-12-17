# Part 1: How many characters need to be processed before the first start-of-packet marker is detected?
# Answer: 1850

# Part 2: How many characters need to be processed before the first start-of-message marker is detected?
# Answer: 2823

# Execution time: 0.220s

def find(lst, num):
    for x in range(len(lst) - num - 1):
        chars = lst[x:x + num]
        if len(chars) == len(set(chars)):
            print("Position of marker for n =", num, ":", x + num)
            break

with open("inputs/6_input.txt") as f:
    for line in f:
        ex = list(line)

    find(ex, 4)
    find(ex, 14)