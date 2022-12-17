# CLEARED 2 STARS

with open("1_input.txt") as f:  
    sums = []
    sum = 0
    for line in f:
        line = line.strip()
        if line == '':
            sums.append(sum)
            sum = 0
            continue
        line = int(line)
        sum += line

print(sums)
newlst = sorted(sums, reverse=True)
print("Maximum calories an elf brought is:", newlst[0])
print("Calories of the top three elves:", newlst[0], newlst[1], newlst[2])
print("Total:", newlst[0] + newlst[1] + newlst[2])