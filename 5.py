# CLEARED 2 STARS

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
with open("5_input.txt") as f:
    for line in f:
        line = line.strip().split(" ")

        if line[0] == "move":
            move = [int(x) for x in line if x.isdigit()]

            for i in range(move[0]):
                crate = stacks[move[1] - 1].pop()
                stacks[move[2] - 1].append(crate)

    s = []
    for stack in stacks:
        s.append(stack.pop())

print("PART 1, Crate number that ends up on top for each stack:", "".join(s))


stacks = [["F", "C", "P", "G", "Q", "R"],
          ["W", "T", "C", "P"],
          ["B", "H", "P", "M", "C"],
          ["L", "T", "Q", "S", "M", "P", "R"],
          ["P", "H", "J", "Z", "V", "G", "N"],
          ["D", "P", "J"],
          ["L", "G", "P", "Z", "F", "J", "T", "R"],
          ["N", "L", "H", "C", "F", "P", "T", "J"],
          ["G", "V", "Z", "Q", "H", "T", "C", "W"]]

# PART 2
with open("5_input.txt") as f:
    for line in f:
        line = line.strip().split(" ")

        if line[0] == "move":
            move = [int(x) for x in line if x.isdigit()]
            stacks[move[2] - 1] += stacks[move[1] - 1][-move[0]:]
            for x in range(move[0]):
                stacks[move[1] - 1].pop()

    s = []
    for stack in stacks:
        s.append(stack.pop())

print("PART 2, Crate number that ends up on top for each stack:", "".join(s))