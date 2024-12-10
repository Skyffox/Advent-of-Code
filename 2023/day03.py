# Part 1: Find all numeric values that are adjacent to a symbol (not the dot).
# Answer: 554003

# Part 2: Find the numeric values of which there are TWO adjacent to the * symbol.
# Answer: 87263515

grid = []
lst = []

def check_value(y, x):
    asterisk_coor = ()
    for y_offset in range(-1, 2):
        for x_offset in range(-1, 2):
            # Search in a 3x3 grid around the coordinate for a symbol.
            if y + y_offset > len(grid)-1 or y + y_offset < 0 or x + x_offset > len(grid[0])-1 or x + x_offset < 0:
                continue

            val = grid[y+y_offset][x+x_offset]
            if not val.isdigit() and not val == '.':
                # Add the coordinate of the asterisk in the return value.
                if val == "*":
                    asterisk_coor = (y+y_offset, x+x_offset)
                
                return True, asterisk_coor
    return False, asterisk_coor


with open("inputs/3_input.txt") as f:
    for y, line in enumerate(f):
        line = line.strip()
        grid.append([x for x in line.strip("")])

        sublst = []
        for x, val in enumerate(line):
            # We want to locate the full number with its coordinates in the grid so we can loop over the coordinates later.
            if val.isdigit():
                sublst.append([val, (y, x)])
            else:
                # Add number and coords to list when a non numeric value was found.
                if sublst != []:
                    num = int(''.join(map(str, [item[0] for item in sublst])))
                    coords = [item[1] for item in sublst]
                    lst.append((num, coords))
                    sublst = []
        
#for loops also have an else clause which most of us are unfamiliar with. The else clause executes after the loop completes normally. 
#This means that the loop did not encounter a break statement. They are really useful once you understand where to use them. I, myself, came to know about them a lot later.

#The common construct is to run a loop and search for an item. If the item is found, we break out of the loop using the break statement. 
#There are two scenarios in which the loop may end. The first one is when the item is found and break is encountered. 
#The second scenario is that the loop ends without encountering a break statement. Now we may want to know which one of these is the reason for a loop’s completion. 
#One method is to set a flag and then check it once the loop ends. Another is to use the else clause.


        # An edge-case when the number is the final value of the line.
        if sublst != []:
            num = int(''.join(map(str, [item[0] for item in sublst])))
            coords = [item[1] for item in sublst]
            lst.append((num, coords))


total = 0
gear_ratio = 0
asterisks = {}
for num in lst:
    for coor in num[1]:
        valid = check_value(coor[0], coor[1])
        # Part 2 - See if number is adjacent to asterisk.
        if valid[1] != ():
            if valid[1] not in asterisks:
                # Add new asterisk coordinate.
                asterisks.update({valid[1] : [num[0]]})
            else:
                # Add number coordinate to existing asterisk.
                asterisks[valid[1]].append(num[0])
        # Part 1
        if valid[0]:
            total += num[0]
            break

# For all asterisks with two adjacent numeric values add the product of the two numbers.
for key, value in asterisks.items():
    if len(value) == 2:
        gear_ratio += (value[0] * value[1])

print("Sum of all part numbers (a part number is a number next to a symbol in the input):", total)
print("Sum of the product of two numbers adjacent to a * symbol:", gear_ratio)