# Part 1: Find the Elf carrying the most Calories.
# Answer: 72240

# Part 2: Find the top three Elves carrying the most Calories.
# Answer: 210957

with open("inputs/1_input.txt") as f:  
    sum_lst = []
    total = 0
    for line in f:
        line = line.strip()
        if line == '':
            sum_lst.append(total)
            total = 0
            continue
        total += int(line)

lst = sorted(sum_lst, reverse=True)
print("Maximum calories an elf brought is:", lst[0])
print("Total top three:", sum(lst[0:3]))