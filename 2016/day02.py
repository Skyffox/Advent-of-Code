# Part 1: Traverse a keypad to punch a specific code
# Answer: 56855

# Part 2: The keypad is different but still same thing
# Answer: B3C27


pos1, pos2 = [2, 2], [2, 2]
# Translate positions on the grid back to a number for the keypad
keypad_part1 = {"1":[1,1], "2":[2,1], "3":[3,1], "4":[1,2], "5":[2,2], "6":[3,2], "7":[1,3], "8":[2,3], "9":[3,3]}
keypad_part2 = {"1":[3,1], "2":[2,2], "3":[3,2], "4":[4,2], "5":[1,3], "6":[2,3], "7":[3,3], "8":[4,3], "9":[5,3], 
                "A":[2,4], "B":[3,4], "C":[4,4], "D":[3,5]}

# Possible movement options for each position on the grid
movement_part1 = {"1":["D", "R"], "2":["L", "R", "D"], "3":["L", "D"], "4":["U", "R", "D"], "5":["U", "D", "L", "R"], 
                  "6":["U", "L", "D"], "7":["U", "R"], "8":["U", "L", "R"], "9":["U", "L"]}
movement_part2 = {"1":["D"], "2":["R", "D"], "3":["U", "D", "L", "R"], "4":["L", "D"], "5":["R"], 
                  "6":["U", "D", "L", "R"], "7":["U", "D", "L", "R"], "8":["U", "D", "L", "R"], "9":["L"], 
                  "A":["U", "R"], "B":["U", "D", "L", "R"], "C":["L", "U"], "D":["U"]}


# Bit dumb, find our keygrid position in the values and get back the key
def dict_value(my_dict, pos):
    return list(my_dict.keys())[list(my_dict.values()).index(pos)]

# Make a move in the grid based on current options
def move(instruction, moves, pos):
    if instruction not in moves:
        return pos
    elif instruction == "U":
        pos[1] -= 1
    elif instruction == "L":
        pos[0] -= 1
    elif instruction == "R":
        pos[0] += 1
    elif instruction == "D":
        pos[1] += 1

    return pos


keylock1, keylock2 = [], []
with open("inputs/2_input.txt") as f:
    for line in f:
        instructions = list(line.strip())

        # Part 1 & 2
        for instruction in instructions:
            # Get the current position on the grid
            number1 = dict_value(keypad_part1, pos1)
            pos1 = move(instruction, movement_part1[number1], pos1)

            number2 = dict_value(keypad_part2, pos2)
            pos2 = move(instruction, movement_part2[number2], pos2)

        keylock1.append(dict_value(keypad_part1, pos1))
        keylock2.append(dict_value(keypad_part2, pos2))

# Make a list of strings to a single number
print("Part 1:", ''.join(map(str, keylock1)))
print("Part 2:", ''.join(map(str, keylock2)))