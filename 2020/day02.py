# Part 1: Find how many passwords are valid
# Answer: 645

# Part 2: The password policy was wrong and the first part of the rule was actually the index at which this letter must occur
# Answer: 737


n, n2 = 0, 0
with open("inputs/2_input.txt") as f:
    for line in f:
        line = line.strip().split(":")

        rule = line[0].split(" ")
        lowerbound, upperbound = rule[0].split("-")
        lowerbound, upperbound = int(lowerbound), int(upperbound)
        password = line[1].strip()

        # Part 1
        if sum([1 for x in password if x == rule[1]]) in range(lowerbound, upperbound + 1):
            n += 1

        # Part 2
        # They do not have a zero-index policy
        if (password[lowerbound - 1] == rule[1] and password[lowerbound - 1] != password[upperbound - 1]) or \
           (password[upperbound - 1] == rule[1] and password[lowerbound - 1] != password[upperbound - 1]):
            n2 += 1

print("Part 1:", n)
print("Part 1:", n2)