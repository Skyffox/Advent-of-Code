# CLEARED 2 STARS

# PART 1
with open("3_input.txt") as f:
    s = 0
    for line in f:
        line = list(line.strip())
        first_compartment = line[:len(line)//2]
        second_compartment = line[len(line)//2:]

        for item in first_compartment:
            if item in second_compartment:
                common = item
                break

        if common.isupper():
            s += ord(common) - 38
        else:
            s += ord(common) - 96

    print("Sum  of priorities of common items:", s)


# PART 2
with open("3_input.txt") as f:
    s = 0
    lines = f.readlines()
    for i in range(0, len(lines), 3):
        for item in lines[i]:
            if item in lines[i+1] and item in lines[i+2]:
                common = item
                break

        if common.isupper():
            s += ord(common) - 38
        else:
            s += ord(common) - 96
        
print("Sum of priorities of badge:", s)