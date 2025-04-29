# pylint: disable=line-too-long
"""
Part 1: A pattern that spirals and we need to find out how many steps we are removed from the center of it
Answer: 552

Part 2: What is the first value written that is larger than your puzzle input, if we assign values to each squares that make up the sum of its neighbours
Answer: 330785
"""

from utils import profiler

PUZZLE_INPUT = 325489


@profiler
def part_1():
    """
    I noticed that the bottom right is always the square of an uneven number, so create enough of these
    anchor points to see where our number is closest to then calculate the Manhattan distance back to 1.
    """
    i = 1
    while i * i < PUZZLE_INPUT:
        i += 2

    pivots = [i * i - k * (i - 1) for k in range(4)]

    for p in pivots:
        dist = abs(p - PUZZLE_INPUT)
        if dist <= (i - 1) // 2:
            return i - 1 - dist


@profiler
def part_2():
    """Recreate a line that circles around where each new value is the sum of its surroundings"""
    # The list values contains all numbers that are already place and their respective coordinates: (x, y, value)
    values = [(0, 0, 1)]

    # To complete one full round in a square we have to move in all 4 directions in this order: +y, -x, -y, +x
    directions = [(0, 1), (-1, 0), (0, -1), (1, 0)]

    # Initial coordinate (center 1) and initial level. The level states how many number are in any side of the current square.
    # It increases by 2 each time a square is completed.
    level = 1
    x, y = 0, 0

    while True:
        for direction in range(4):
            # Get the current direction we have to move in the X and Y axis
            dir_x, dir_y = directions[direction]

            # Since we are moving in a spiral we don't have to move the same number of steps in each direction.
            # The first number of the next square is always placed by the previous level -> the first iteration where level = 1
            # places only the number 1 at x=1, y=0. Then in level = 3 we start from x=1 and y=0 and move 1 step in y+ (direction = 0),
            # 2 steps in x- (direction = 1) and 2 steps in y- (direction = 2). In last direction x+ we move 3 steps and out into the next square.
            if direction == 0:
                move_n = level - 2
            elif direction in [1, 2]:
                move_n = level - 1
            else:
                move_n = level

            for _ in range(move_n):
                x += dir_x
                y += dir_y

                # In this list comprehension all values in the values list are summed up where the x and the y coordinate is not more than 1 off from
                # the current coordinate (if abs(x-k[0]) <= 1 and abs(y-k[1]) <= 1)
                new = sum([k[2] for k in values if abs(x-k[0]) <= 1 and abs(y-k[1]) <= 1])

                # Add the new value and its coordinates to the list
                values.append((x, y, new))

                # Check if our input number is reached.
                if new >= PUZZLE_INPUT:
                    return new

        # Increase the level by 2 for the next iteration
        level += 2


if __name__ == "__main__":
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")
