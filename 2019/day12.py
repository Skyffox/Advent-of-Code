# pylint: disable=line-too-long
"""
Day 12: The N-Body Problem

Part 1: What is the total energy in the system after simulating the moons given in your scan for 1000 steps?
Answer: 7138

Part 2: How many steps does it take to reach the first state that exactly matches a previous state?
Answer: 572087463375796
"""

import re
from typing import List, Tuple
from math import gcd
from utils import profiler


class Moon:
    """
    Represents a moon in 3D space with position and velocity vectors.

    Each moon has:
    - A position vector `pos` as a list of three integers [x, y, z].
    - A velocity vector `vel` initialized to [0, 0, 0].
    """

    def __init__(self, pos: Tuple[int, int, int]):
        self.pos = list(pos) # [x, y, z]
        self.vel = [0, 0, 0]

    def potential_energy(self) -> int:
        """Calculates the potential energy (sum of absolute position components)."""
        return sum(abs(c) for c in self.pos)

    def kinetic_energy(self) -> int:
        """Calculates the kinetic energy (sum of absolute velocity components)."""
        return sum(abs(c) for c in self.vel)

    def total_energy(self) -> int:
        """Calculates the total energy as potential energy × kinetic energy."""
        return self.potential_energy() * self.kinetic_energy()


def get_input(file_path: str) -> List[Tuple[int, int, int]]:
    """
    Reads the input file and returns a list of tuples representing the positions of the moons.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        List[Tuple[int, int, int]]: A list of tuples representing the positions of the moons.
    """
    positions = []
    pattern = re.compile(r"<x=(-?\d+), y=(-?\d+), z=(-?\d+)>")

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            match = pattern.match(line)
            if match:
                x, y, z = map(int, match.groups())
                positions.append((x, y, z))

    return positions


def lcm(a: int, b: int) -> int:
    """
    Calculates the least common multiple of two numbers.

    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        int: The least common multiple of the two numbers.
    """
    return abs(a * b) // gcd(a, b)


def apply_gravity(moons: List[Moon]):
    """
    Applies gravity to the moons, updating their velocities.

    Args:
        moons (List[Tuple[int, int, int]]): A list of tuples representing the positions of the moons.

    Returns:
        List[Tuple[int, int, int]]: A list of tuples representing the updated velocities of the moons.
    """
    for i, moon_a in enumerate(moons):
        for _, moon_b in enumerate(moons[i + 1:], start=i + 1):
            for axis in range(3):
                if moon_a.pos[axis] < moon_b.pos[axis]:
                    moon_a.vel[axis] += 1
                    moon_b.vel[axis] -= 1
                elif moon_a.pos[axis] > moon_b.pos[axis]:
                    moon_a.vel[axis] -= 1
                    moon_b.vel[axis] += 1


def apply_velocity(moons: List[Moon]):
    """
    Applies velocity to the moons, updating their positions.

    Args:
        moons (List[Tuple[int, int, int]]): A list of tuples representing the positions of the moons.
        velocities (List[Tuple[int, int, int]]): A list of tuples representing the velocities of the moons.

    Returns:
        List[Tuple[int, int, int]]: A list of tuples representing the updated positions of the moons.
    """
    for moon in moons:
        for axis in range(3):
            moon.pos[axis] += moon.vel[axis]


@profiler
def part_one(data_input: List[Tuple[int, int, int]]) -> int:
    """
    Solves part one of the problem using the provided input data.

    Args:
        data_input (List[Tuple[int, int, int]]): A list of tuples representing the positions of the moons.

    Returns:
        int: The total energy of the system after 1000 steps.
    """
    moons = [Moon(pos) for pos in data_input]
    for _ in range(1000):
        apply_gravity(moons)
        apply_velocity(moons)
    return sum(moon.total_energy() for moon in moons)


@profiler
def part_two(data_input: List[Tuple[int, int, int]]) -> int:
    """
    Solves part two of the problem using the provided input data.

    Args:
        data_input (List[Tuple[int, int, int]]): A list of tuples representing the positions of the moons.

    Returns:
        int: The number of steps required for the system to reach a state where all positions and velocities repeat.
    """
    moons = [Moon(pos) for pos in data_input]
    # For each axis independently
    initial_states = []
    for axis in range(3):
        state = []
        for moon in moons:
            state.append((moon.pos[axis], moon.vel[axis]))
        initial_states.append(tuple(state))

    steps = [0, 0, 0]

    # We simulate each axis independently, create separate copies for each axis
    positions = [[moon.pos[axis] for moon in moons] for axis in range(3)]
    velocities = [[moon.vel[axis] for moon in moons] for axis in range(3)]

    found = [False, False, False]
    step = 0

    while not all(found):
        step += 1

        for axis in range(3):
            if found[axis]:
                continue
            # Apply gravity
            for i in range(len(moons)):
                for j in range(i+1, len(moons)):
                    if positions[axis][i] < positions[axis][j]:
                        velocities[axis][i] += 1
                        velocities[axis][j] -= 1
                    elif positions[axis][i] > positions[axis][j]:
                        velocities[axis][i] -= 1
                        velocities[axis][j] += 1
            # Apply velocity
            for i in range(len(moons)):
                positions[axis][i] += velocities[axis][i]

            # Check if axis matches initial state
            current_state = tuple((positions[axis][i], velocities[axis][i]) for i in range(len(moons)))
            if current_state == initial_states[axis]:
                found[axis] = True
                steps[axis] = step

    # Return LCM of the three axis cycle lengths
    return lcm(lcm(steps[0], steps[1]), steps[2])


if __name__ == "__main__":
    input_data = get_input("inputs/12_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
