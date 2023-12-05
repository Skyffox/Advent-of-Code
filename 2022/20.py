# Part 1:
# Answer:

# Part 2:
# Answer: 

# Execution time: 

from copy import deepcopy

initial = []
idx = 0
with open("inputs/20_input.txt") as f:
    for line in f:
        line = line.strip()
        initial.append([int(line), idx])
        idx += 1

tmp = deepcopy([x[0] for x in initial])
for idx, [num, tmp_idx] in enumerate(initial):
    wrap_idx = num + tmp_idx
    if num == 0:
        continue
    elif num > 0:
        del tmp[tmp_idx]
        if wrap_idx > len(initial):
            wrap_idx = (wrap_idx) % len(initial) + 1
            tmp.insert(wrap_idx, num)
        elif wrap_idx == len(initial):
            wrap_idx = 0
            tmp.insert(wrap_idx, num)
        else:
            tmp.insert(wrap_idx, num)
        
        initial[idx][1] = wrap_idx
        # Index has wrapped and moved to the left so everything on the right must move +1
        if wrap_idx < tmp_idx:
            for enum_idx, [num, init_idx] in enumerate(initial):
                if init_idx >= wrap_idx and init_idx <= tmp_idx and enum_idx != idx:
                    initial[enum_idx][1] += 1

        # Moved to the right, from old postion to new position on the left must move 
        if wrap_idx > tmp_idx:
            for enum_idx, [_, init_idx] in enumerate(initial):
                if init_idx >= tmp_idx and init_idx <= wrap_idx and enum_idx != idx:
                    initial[enum_idx][1] -= 1

    else:
        del tmp[tmp_idx]
        if wrap_idx < 0:
            wrap_idx = wrap_idx % len(initial) - 1
            tmp.insert(wrap_idx, num)
        elif wrap_idx == 0:
            wrap_idx = len(initial) - 1
            tmp.insert(wrap_idx, num)
        else:        
            tmp.insert(wrap_idx, num)

        initial[idx][1] = wrap_idx
        # Index has wrapped and moved to the left so everything on the right must move +1
        if wrap_idx < tmp_idx:
            for enum_idx, [num, init_idx] in enumerate(initial):
                if init_idx >= wrap_idx and init_idx <= tmp_idx and enum_idx != idx:
                    initial[enum_idx][1] += 1

        # Moved to the right, from old postion to new position on the left must move 
        if wrap_idx > tmp_idx:
            for enum_idx, [_, init_idx] in enumerate(initial):
                if init_idx >= tmp_idx and init_idx <= wrap_idx and enum_idx != idx:
                    initial[enum_idx][1] -= 1
    
    
zero_pos = [idx for idx, x in enumerate(tmp) if x == 0][0] - 1
x_coor = tmp[((1000 - zero_pos) % len(tmp))]
y_coor = tmp[((2000 - zero_pos) % len(tmp))]
z_coor = tmp[((3000 - zero_pos) % len(tmp))]

print("Sum of the three coordinates:", x_coor + y_coor + z_coor)