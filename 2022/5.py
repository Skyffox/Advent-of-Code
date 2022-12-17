# Part 1: After the rearrangement procedure completes, what crate ends up on top of each stack?
# Answer: DHBJQJCCW

# Part 2: After the rearrangement procedure completes, what crate ends up on top of each stack?
# Answer: WJVRLSJJT

# Execution time: 0.220s

import copy

stacks = [["F", "C", "P", "G", "Q", "R"],
          ["W", "T", "C", "P"],
          ["B", "H", "P", "M", "C"],
          ["L", "T", "Q", "S", "M", "P", "R"],
          ["P", "H", "J", "Z", "V", "G", "N"],
          ["D", "P", "J"],
          ["L", "G", "P", "Z", "F", "J", "T", "R"],
          ["N", "L", "H", "C", "F", "P", "T", "J"],
          ["G", "V", "Z", "Q", "H", "T", "C", "W"]]

# PART 1
def part1(lines, stacks):
    for i in range(0, len(lines)):
        line = list(lines[i].strip().split(" "))

        if line[0] == "move":
            move = [int(x) for x in line if x.isdigit()]

            for i in range(move[0]):
                crate = stacks[move[1] - 1].pop()
                stacks[move[2] - 1].append(crate)

    return stacks

# PART 2
def part2(lines, stacks):
    for i in range(0, len(lines)):
        line = list(lines[i].strip().split(" "))

        if line[0] == "move":
            move = [int(x) for x in line if x.isdigit()]
            stacks[move[2] - 1] += stacks[move[1] - 1][-move[0]:]
            for x in range(move[0]):
                stacks[move[1] - 1].pop()

    return stacks


with open("inputs/5_input.txt") as f:
    lines = f.readlines()

tmp = copy.deepcopy(stacks)
p1 = part1(lines, stacks)
p2 = part2(lines, tmp)
print("PART 1, Crate number that ends up on top for each stack:", "".join([s.pop() for s in p1]))
print("PART 2, Crate number that ends up on top for each stack:", "".join([s.pop() for s in p2]))




