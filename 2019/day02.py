# Part 1: 
# Answer: 

# Part 2: 
# Answer: 


def operation(op, x, y):
    if op == 1:
        return x + y
    if op == 2:
        return x * y


with open("inputs/2_input.txt") as f:
    for line in f:
        instructions = list(map(int, line.strip().split(",")))
    
    # Part 1
    # Below is the working computer however for part 1 they wanted to replace position 1 with the 
    # value 12 and replace position 2 with the value 2.
    instructions[1] = 12
    instructions[2] = 2

    for idx in range(len(instructions) // 4):
        operator = instructions[idx*4]
        x = instructions[idx*4+1]
        y = instructions[idx*4+2]
        output_idx = instructions[idx*4+3]
        
        if operator == 99:
            break
        
        instructions[output_idx] = operation(operator, instructions[x], instructions[y])

print(instructions)

print("Part 1:", instructions[0])
print("Part 2:", )