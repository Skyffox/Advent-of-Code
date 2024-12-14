# pylint: disable=line-too-long
"""
Part 1: 
Answer: 

Part 2: 
Answer: 
"""

import re
from utils import profiler


def get_input(file_path: str) -> list:
    """Get the input data"""
    positions, velocities = [], []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            # Find all ocurences in input of num, num (may contain negative numbers)
            curr_line = re.findall(r'-?\d+,-?\d+', line)
            positions.append(list(map(int, curr_line[0].split(","))))
            velocities.append(list(map(int, curr_line[1].split(","))))

    return positions, velocities


def print_grid(positions, max_width, max_length):
    for l in range(max_length):
        for w in range(max_width):
            if [w, l] in positions:
                print(positions.count([w, l]), end="")
            else:
                print(".", end="")
        print()
    print()

import time

@profiler
def part_one(positions, velocities):
    """Comment"""
    MAX_WIDTH = 101
    MAX_LENGTH = 103
    SECONDS = 10000

    for s in range(SECONDS):
        for idx, (p, v) in enumerate(zip(positions, velocities)):
            # calculate new pos based on velocity and then see if we wrap around a side of the grid
            new_pos = [p[0] + v[0], p[1] + v[1]]
            if new_pos[0] < 0:
                new_pos[0] = new_pos[0] + MAX_WIDTH
            if new_pos[1] < 0:
                new_pos[1] = new_pos[1] + MAX_LENGTH
            if new_pos[0] >= MAX_WIDTH:
                new_pos[0] %= MAX_WIDTH
            if new_pos[1] >= MAX_LENGTH:
                new_pos[1] %= MAX_LENGTH

            positions[idx] = new_pos

        # print if we find more than 15 "1" in a row
        for l in range(MAX_LENGTH):
            robots = sum([1 for r in positions if r[1] == l])
            if robots > 15:
                # Print for debugging pruposes
                print("SECOND:", s)
                print_grid(positions, MAX_WIDTH, MAX_LENGTH)
                time.sleep(1)
                break

    # calculate each guard in each quadrant
    first, second, third, fourth = 0, 0, 0, 0

    for p in positions:
        # upper quadrant
        if p[1] < (MAX_LENGTH - 1) // 2:
            # topleft
            if p[0] < (MAX_WIDTH - 1) // 2:
                first += 1
            # topright
            elif p[0] > (MAX_WIDTH - 1) // 2:
                second += 1

        # lower quadrant
        elif p[1] > (MAX_LENGTH - 1) // 2:
            # bottomleft
            if p[0] < (MAX_WIDTH - 1) // 2:
                third += 1
            # bottomright
            elif p[0] > (MAX_WIDTH - 1) // 2:
                fourth += 1

    return first * second * third * fourth


@profiler
def part_two(positions, velocities):
    """Comment"""
    # LITERALLY DID THIS THROUGH THE PRINTGRID FUNCTION I MADE, here i will just print the grid after the amount of seconds i found
    # 6875 amount of seconds, and print grid i guess to confirm

if __name__ == "__main__":
    # Get input data
    input_positions, input_velocities = get_input("inputs/14_input.txt")

    print(f"Part 1: {part_one(input_positions, input_velocities)}")
    print(f"Part 2: {part_two(input_positions, input_velocities)}")
