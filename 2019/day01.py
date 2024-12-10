# pylint: disable=line-too-long
"""
Part 1: Find the fuel required for each module
Answer: 3296269

Part 2: The extra fuel we take with us makes extra mass which needs extra fuel etc...
Answer: 4941547
"""

from utils import profiler


def get_input(file_path: str) -> list:
    """Get the input data"""
    mass = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            mass.append(int(line.strip()))

    return mass


def fuel_calc(m):
    """Calculate the new amount of mass after adding fuel"""
    return m // 3 - 2


@profiler
def part_1(mass: list) -> int:
    """Calculate the fuel needed for all modules"""
    return sum([fuel_calc(m) for m in mass])


@profiler
def part_2(mass: list) -> int:
    """If we get more fuel that adds more weight thus needing more fuel"""
    n = 0
    for m in mass:
        while True:
            m = fuel_calc(m)
            if m <= 0:
                break
            n += m

    return n


if __name__ == "__main__":
    input_data = get_input("inputs/1_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
