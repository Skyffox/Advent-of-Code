# pylint: disable=line-too-long
"""
Part 1: What is the Manhattan distance from the central port to the closest intersection?
Answer: 3247

Part 2: What is the fewest combined steps the wires must take to reach an intersection?
Answer: 48054
"""

from utils import profiler


def get_input(file_path: str) -> tuple[list, list]:
    """Get the input data"""
    wires = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = list(line.strip().split(","))
            # Separate the direction and amount we move
            line = [[l[0], int(l[1:])] for l in line]
            wires.append(line)

    return wires


def get_path(instructions):
    """Add the new position to the path"""
    x, y = 0, 0
    path = []

    for direction, steps in instructions:
        for _ in range(steps):
            if direction == 'U':
                y += 1
            elif direction == 'D':
                y -= 1
            elif direction == 'L':
                x -= 1
            elif direction == 'R':
                x += 1

            path.append((x, y))

    return path


@profiler
def part_1(wires: list) -> int:
    """Get all the intersections of the two wires, then calculate the distance to each intersection"""
    # Get the paths for both wires
    path1 = get_path(wires[0])
    path2 = get_path(wires[1])

    # Find the intersections (excluding the origin)
    intersections = set(path1).intersection(set(path2))
    intersections.discard((0, 0))

    # Calculate Manhattan distance for each intersection
    return min(abs(x) + abs(y) for x, y in intersections)


@profiler
def part_2(wires: list) -> int:
    """Get all the intersections of the two wires, then calculate the distance to the closest intersection"""
    # Get the paths for both wires
    path1 = get_path(wires[0])
    path2 = get_path(wires[1])

    # Find the intersections (excluding the origin)
    intersections = set(path1).intersection(set(path2))
    intersections.discard((0, 0))

    # We do +2 because of 0 indexing
    return min([path1.index(x) + path2.index(x) + 2 for x in intersections])


if __name__ == "__main__":
    input_data = get_input("inputs/3_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
