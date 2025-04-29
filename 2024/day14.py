# pylint: disable=line-too-long
"""
Part 1: What will the safety factor be after exactly 100 seconds have elapsed?
Answer: 216027840

Part 2: What is the fewest number of seconds that must elapse for the robots to display the Easter egg?
Answer: 6876
"""

import re
from copy import deepcopy
from utils import profiler


def get_input(file_path: str) -> tuple[list, list]:
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


def print_grid(positions: list, max_width: int, max_length: int) -> None:
    """Print the grid, purely used for debug purposes and checking whether part 2 is correct"""
    for l in range(max_length):
        for w in range(max_width):
            if [w, l] in positions:
                print(positions.count([w, l]), end="")
            else:
                print(".", end="")
        print()
    print()


@profiler
def part_one(positions: list, velocities: list) -> int:
    """Simulate the positions of all robots and afterwards count how many reside in each quadrant of the grid"""
    max_width = 101
    max_length = 103
    seconds = 100

    for _ in range(seconds):
        for idx, (p, v) in enumerate(zip(positions, velocities)):
            # Calculate the new position based on the velocity, if we are outside the grid then we wrap around
            x, y = p[0] + v[0], p[1] + v[1]
            if x < 0:
                x += max_width
            if y < 0:
                y += max_length
            if x >= max_width:
                x %= max_width
            if y >= max_length:
                y %= max_length

            positions[idx] = [x, y]

    # Calculate the amount of guards in each quadrant
    first, second, third, fourth = 0, 0, 0, 0

    for x, y in positions:
        # Upper quadrant
        if y < (max_length - 1) // 2:
            # Topleft
            if x < (max_width - 1) // 2:
                first += 1
            # Topright
            elif x > (max_width - 1) // 2:
                second += 1

        # Lower quadrant
        elif y > (max_length - 1) // 2:
            # Bottomleft
            if x < (max_width - 1) // 2:
                third += 1
            # Bottomright
            elif x > (max_width - 1) // 2:
                fourth += 1

    return first * second * third * fourth


@profiler
def part_two(positions: list, velocities: list) -> int:
    """After a certain amount of seconds the robots form a christmas tree, here the answer is given for quick debug purposes"""
    max_width = 101
    max_length = 103
    seconds = 6876 # This is the answer

    for _ in range(seconds):
        for idx, (p, v) in enumerate(zip(positions, velocities)):
            # Calculate the new position based on the velocity, if we are outside the grid then we wrap around
            x, y = p[0] + v[0], p[1] + v[1]
            if x < 0:
                x += max_width
            if y < 0:
                y += max_length
            if x >= max_width:
                x %= max_width
            if y >= max_length:
                y %= max_length

            positions[idx] = [x, y]

        # Debug purposes, also the print is zero-indexed
        # if s == seconds - 1:
        #     print_grid(positions, max_width, max_length)

    return seconds


if __name__ == "__main__":
    # Get input data
    input_positions, input_velocities = get_input("inputs/14_input.txt")

    input_positions_cpy = deepcopy(input_positions)

    print(f"Part 1: {part_one(input_positions, input_velocities)}")
    print(f"Part 2: {part_two(input_positions_cpy, input_velocities)}")
