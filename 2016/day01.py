# pylint: disable=line-too-long
"""
Part 1: See how many blocks we are away from the start after following instructions
Answer: 252

Part 2: Check for a path and see where we have been before
Answer: 143
"""

from utils import profiler


def move(orientation, direction, distance, pos, visited):
    """A"""
    # Some cases we move in the same direction
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


def get_input(file_path: str) -> tuple[list, list]:
    """Get the input data"""
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            instructions = line.strip().split(", ")

    return instructions


@profiler
def part_1(instructions: list) -> int:
    """a"""
    pos = [0, 0]
    visited = [[0, 0]]
    orientation = "N"

    for instruction in instructions:
        instruction = [c for c in instruction]
        orientation, pos, visited = move(orientation, instruction[0], int("".join(instruction[1:])), pos, visited)

    return abs(pos[0]) + abs(pos[1]), visited


@profiler
def part_2(visited: list) -> int:
    """a"""
    for idx, v2 in enumerate(visited):
        # See what position occurs in the rest of the list
        if v2 in visited[idx+1:]:
            return abs(v2[0]) + abs(v2[1])


if __name__ == "__main__":
    instr = get_input("inputs/1_input.txt")

    ans, v = part_1(instr)

    print(f"Part 1: {ans}")
    print(f"Part 2: {part_2(v)}")
