# pylint: disable=line-too-long
"""
Part 1: Simulate your complete hypothetical series of motions. How many positions does the tail of the rope visit at least once?
Answer: 6175

Part 2: Simulate your complete series of motions on a larger rope with ten knots. How many positions does the tail of the rope visit at least once?
Answer: 2578
"""

from utils import profiler


def get_input(file_path: str) -> list:
    """Get the input data"""
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]


def move_tail(lead, follow) -> tuple[int, int]:
    """
    This function moves the tail knot towards the head knot if they are not adjacent. 
    It adjusts the tail's position by one step in the x or y direction, 
    depending on the difference between the head and tail's coordinates.
    """
    if abs(lead[0] - follow[0]) <= 1 and abs(lead[1] - follow[1]) <= 1:
        return follow

    xdiff = lead[0] - follow[0]
    ydiff = lead[1] - follow[1]

    # If in same column or longer distance by Y axis
    if xdiff == 0 or abs(xdiff) < abs(ydiff):
        return (lead[0], lead[1] - 1 if ydiff > 0 else lead[1] + 1)

    # If in same row or longer distance by X axis
    if ydiff == 0 or abs(xdiff) > abs(ydiff):
        return (lead[0] - 1 if xdiff > 0 else lead[0] + 1, lead[1])

    return (lead[0] - 1 if xdiff > 0 else lead[0] + 1,
            lead[1] - 1 if ydiff > 0 else lead[1] + 1)


@profiler
def simulate_rope_movements(instructions, num_knots):
    """
    This function simulates the movement of the rope's knots based on the input instructions. 
    It updates the position of each knot and tracks the unique positions visited by the last knot (the tail).
    For each instruction, we first move the head knot according to the direction (U, D, L, R). 
    Then, we move the rest of the knots towards the knot ahead of them. The last knot's position is recorded in a set of visited positions.
    """
    # Start with the head at [0, 0] and all knots at [0, 0]
    knots = [[0, 0]] * num_knots
    visited_positions = set()
    # Initially, the tail is at (0, 0)
    visited_positions.add(tuple(knots[-1]))

    # Directions: U = up, D = down, L = left, R = right
    direction_map = {
        'U': (0, 1),
        'D': (0, -1),
        'L': (-1, 0),
        'R': (1, 0)
    }

    for instruction in instructions:
        direction, steps = instruction.split()
        steps = int(steps)
        # Move the head knot
        for _ in range(steps):
            # Move head
            head_x, head_y = knots[0]
            move_x, move_y = direction_map[direction]
            knots[0] = [head_x + move_x, head_y + move_y]

            # Move the tail(s)
            for i in range(1, len(knots)):
                knots[i] = move_tail(knots[i-1], knots[i])

            # Track the position of the last knot (the tail)
            visited_positions.add(tuple(knots[-1]))

    return len(visited_positions)


if __name__ == "__main__":
    input_data = get_input("inputs/9_input.txt")

    print(f"Part 1: {simulate_rope_movements(input_data, 2)}")
    print(f"Part 2: {simulate_rope_movements(input_data, 10)}")
