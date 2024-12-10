# Part 1: Find the fuel required for each module
# Answer: 3296269

# Part 2: The extra fuel we take with us makes extra mass which needs extra fuel etc...
# Answer: 4941547

# Calculate the fuel needed based on the amount of mass
def fuel_calc(m):
    return m // 3 - 2

n, n2 = 0, 0
with open("inputs/1_input.txt") as f:
    for line in f:
        # Part 1
        mass = int(line.strip())

        # Fuel required equals: mass // 3 - 2
        n += fuel_calc(mass)

        # Part 2
        while True:
            mass = fuel_calc(mass)
            if mass <= 0:
                break
            n2 += mass


print("Part 1:", n)
print("Part 2:", n2)