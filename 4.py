# CLEARED 2 STARS

with open("4_input.txt") as f:
    count = 0
    count2 = 0
    for line in f:
        line = line.strip().split(",")
        elf1 = line[0].split("-")
        elf2 = line[1].split("-")

        # PART 1
        if int(elf1[0]) >= int(elf2[0]) and int(elf1[1]) <= int(elf2[1]):
            count += 1

        elif int(elf2[0]) >= int(elf1[0]) and int(elf2[1]) <= int(elf1[1]):
            count += 1

        # PART 2
        r1 = range(int(elf1[0]), int(elf1[1]) + 1)
        r2 = range(int(elf2[0]), int(elf2[1]) + 1)
        for r in r1:
            if r in r2:
                count2 += 1
                break

print("Assignment pairs that fully contain each other", count)
print("Assignment pairs that overlap", count2)