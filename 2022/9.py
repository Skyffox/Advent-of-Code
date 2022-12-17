# Part 1: How many positions does the tail of the rope visit at least once?
# Answer: 13

# Part 2: Simulate your complete series of motions on a larger rope with ten knots. How many positions does the tail of the rope visit at least once?
# Answer: ???

# Execution time: ???

# NOTE: only works with small grid
def print_grid(min_x, min_y, max_x, max_y, headpos, tailpos, prev_tail_pos, command=None, part2=[]):
    if command is None:
        print("== Initial State ==")
        print()
    else:
        print("==", command[0], command[1], "==")
        print()

    for y in range(max_y - 1, min_y - 1, -1):
        for x in range(min_x, max_x):
            if part2 != []:
                if [x, y] == headpos:
                    print("H ", end="")
                elif [x, y] == tailpos and tailpos != headpos:
                    print("T ", end="")
                elif [x, y] == [0, 0] and ([0, 0] != headpos or [0, 0] != tailpos):
                    print("s ", end="")
                elif [x, y] in prev_tail_pos and ([x, y] != headpos or [x, y] != tailpos):
                    print("# ", end="")
                else:
                    print(". ", end="")
            else:
                if [x, y] in part2:
                    i = [x for x in part2 if [x, y] == x][0]
                    print(i, end="")
                elif [x, y] in prev_tail_pos and ([x, y] != headpos or [x, y] != tailpos):
                    print("# ", end="")
                else:
                    print(". ", end="")
        print()
    print()


def move(command, hpos, tpos, tail_positions):
    dir, dist = command
    for _ in range(dist):
        if dir == "R":
            if hpos[0] - tpos[0] < 1:
                hpos[0] += 1
            elif hpos[1] - tpos[1] == 0:
                if hpos[0] - tpos[0] < 1:
                    hpos[0] += 1
                else:
                    hpos[0] += 1
                    tpos[0] += 1
            elif hpos[0] - tpos[0] > 0:
                hpos[0] += 1
                tpos[0] += 1
                if hpos[1] - tpos[1] > 0:
                    tpos[1] += 1
                else:
                    tpos[1] -= 1

        elif dir == "L":
            if hpos[0] - tpos[0] > -1:
                hpos[0] -= 1
            elif hpos[1] - tpos[1] == 0:
                if hpos[0] - tpos[0] > -1:
                    hpos[0] -= 1
                else:
                    hpos[0] -= 1
                    tpos[0] -= 1
            elif hpos[0] - tpos[0] < 0:
                hpos[0] -= 1
                tpos[0] -= 1
                if hpos[1] - tpos[1] < 0:
                    tpos[1] -= 1
                else:
                    tpos[1] += 1

        elif dir == "U":
            if hpos[1] - tpos[1] < 1:
                hpos[1] += 1
            elif hpos[0] - tpos[0] == 0:
                if hpos[1] - tpos[1] < 1:
                    hpos[1] += 1
                else:
                    hpos[1] += 1
                    tpos[1] += 1
            elif hpos[1] - tpos[1] > 0:
                hpos[1] += 1
                tpos[1] += 1
                if hpos[0] - tpos[0] > 0:
                    tpos[0] += 1
                else:
                    tpos[0] -= 1

        elif dir == "D":
            if hpos[1] - tpos[1] > -1:
                hpos[1] -= 1
            elif hpos[0] - tpos[0] == 0:
                if hpos[1] - tpos[1] > -1:
                    hpos[1] -= 1
                else:
                    hpos[1] -= 1
                    tpos[1] -= 1
            elif hpos[1] - tpos[1] < 0:
                hpos[1] -= 1
                tpos[1] -= 1
                if hpos[0] - tpos[0] < 0:
                    tpos[0] -= 1
                else:
                    tpos[0] += 1

        tail_positions.append(tpos[::])
        # print_grid(0, 0, 6, 5, hpos, tpos, tail_positions, c)
    return tail_positions, hpos, tpos


# PART 1
commands = []
with open("inputs/9_input.txt") as f:
    for line in f:
        line = line.strip().split(" ")
        commands.append((line[0], int(line[1])))

hpos = [0, 0]
tpos = [0, 0]
tail_positions = [[0, 0]]
for c in commands:
    for _ in range(c[1]):
        tail_positions, hpos, tpos = move((c[0], 1), hpos, tpos, tail_positions)

unique_pos = [list(x) for x in set(tuple(x) for x in tail_positions)]
print("Number of unique tail positions:", len(unique_pos))


# PART 2
# pos = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
# tail_positions = [[0, 0]]
# for c in commands:
#     for _ in range(c[1]):
#         # head always moves
#         tail_positions, pos[0], pos[1] = move((c[0], 1), pos[0], pos[1], tail_positions)
#         for i in range(2, 9):
#             # either moves all or twice
#             # TODO such that the head only
#             tail_positions, pos[i], pos[i+1] = move((c[0], 1), pos[i], pos[i+1], tail_positions)
#         print(pos)
#         # break
#     break
#         # print_grid(0, 0, 6, 5, [], [], tail_positions, c, pos)


# print("Number of unique tail positions for 10 tails:")