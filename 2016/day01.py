# pylint: disable=line-too-long
"""
Part 1: See how many blocks we are away from the start after following instructions
Answer: 252

Part 2: Check for a path and see where we have been before
Answer: 143
"""

from utils import profiler


def move(orientation: str, direction: str, distance: int, pos: tuple[int, int], visited: list) -> tuple[str, tuple[int, int], list]:
    """
    Our new orientation is based on our current orientation and the direction from the input. Then move a
    In that new direction for an amount of steps equal to distance and add these new positions to visited.
    """
    if (orientation == "N" and direction == "L") or (orientation == "S" and direction == "R"):
        orientation = "W"
        for x in range(pos[0], pos[0] - distance, -1):
            pos[0] -= 1
            visited.append([x-1, pos[1]]) 

    elif (orientation == "N" and direction == "R") or (orientation == "S" and direction == "L"):
        orientation = "E"
        for x in range(pos[0], pos[0] + distance):
            pos[0] += 1
            visited.append([x+1, pos[1]]) 

    elif (orientation == "W" and direction == "L") or (orientation == "E" and direction == "R"):
        orientation = "S"
        for y in range(pos[1], pos[1] - distance, -1):
            pos[1] -= 1
            visited.append([pos[0], y-1]) 

    elif (orientation == "E" and direction == "L") or (orientation == "W" and direction == "R"):
        orientation = "N"
        for y in range(pos[1], pos[1] + distance):
            pos[1] += 1
            visited.append([pos[0], y+1])

    return orientation, pos, visited


def get_input(file_path: str) -> list:
    """Get the input data"""
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            return line.strip().split(", ")


@profiler
def part_1(instructions: list) -> int:
    """Execute each instruction which will move us in a certain direction for an amount of steps"""
    pos = [0, 0]
    visited = [[0, 0]]
    orientation = "N"

    for instruction in instructions:
        orientation, pos, visited = move(orientation, instruction[0], int("".join(instruction[1:])), pos, visited)

    # Return what positions we visited, as we need it for part 2
    return abs(pos[0]) + abs(pos[1]), visited


@profiler
def part_2(visited: list) -> int:
    """See if we have visited a position prior"""
    positions = set()
    for pos in visited:
        if tuple(pos) in positions:
            return abs(pos[0]) + abs(pos[1])

        positions.add(tuple(pos))


if __name__ == "__main__":
    instr = get_input("inputs/1_input.txt")

    ans, v = part_1(instr)

    print(f"Part 1: {ans}")
    print(f"Part 2: {part_2(v)}")
