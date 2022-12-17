# CLEARED 2 STARS

def find(lst, num):
    for x in range(len(lst) - num - 1):
        chars = lst[x:x+num]
        if len(chars) == len(set(chars)):
            print("Position of marker for n =", num, ":", x+num)
            break

with open("6_input.txt") as f:
    for line in f:
        ex = list(line)

    find(ex, 4)
    find(ex, 14)