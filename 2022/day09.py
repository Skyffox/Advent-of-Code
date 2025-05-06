# pylint: disable=line-too-long
"""
Day 9: Rope Bridge

Part 1: Simulate your complete hypothetical series of motions. How many positions does the tail of the rope visit at least once?
Answer: 6175

Part 2: Simulate your complete series of motions on a larger rope with ten knots. How many positions does the tail of the rope visit at least once?
Answer: 2578
"""

from utils import profiler


def get_input(file_path: str) -> list:
    """
    Reads the input data from the specified file and returns a list of instructions.

    Each instruction represents a movement command in the format "DIRECTION STEPS", where:
    - DIRECTION is one of 'U', 'D', 'L', or 'R' (up, down, left, right).
    - STEPS is the number of steps the head of the rope moves in the specified direction.

    Args:
        file_path (str): The path to the input file containing the rope movement instructions.

    Returns:
        list: A list of strings, where each string contains a direction and step count.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]


def move_tail(lead, follow) -> tuple[int, int]:
    """
    Moves the tail knot towards the head knot if they are not adjacent. 

    This function adjusts the tail's position by one step in the x or y direction 
    to bring it closer to the head knot. The tail moves one unit along the axis where 
    the difference between the head and tail is greatest.

    Args:
        lead (tuple): The coordinates of the lead knot (head), represented as a tuple (x, y).
        follow (tuple): The coordinates of the tail knot, also represented as a tuple (x, y).

    Returns:
        tuple[int, int]: The new position of the tail knot (x, y).
    """
    if abs(lead[0] - follow[0]) <= 1 and abs(lead[1] - follow[1]) <= 1:
        return follow  # No movement needed if the knots are adjacent

    xdiff = lead[0] - follow[0]
    ydiff = lead[1] - follow[1]

    # Move along the Y axis if it's a longer distance
    if xdiff == 0 or abs(xdiff) < abs(ydiff):
        return (lead[0], lead[1] - 1 if ydiff > 0 else lead[1] + 1)

    # Move along the X axis if it's a longer distance
    if ydiff == 0 or abs(xdiff) > abs(ydiff):
        return (lead[0] - 1 if xdiff > 0 else lead[0] + 1, lead[1])

    # Move diagonally if needed
    return (lead[0] - 1 if xdiff > 0 else lead[0] + 1,
            lead[1] - 1 if ydiff > 0 else lead[1] + 1)


@profiler
def simulate_rope_movements(instructions, num_knots):
    """
    Simulates the movement of a rope's knots based on the given instructions.

    The rope starts with the head and all knots at position (0, 0). For each instruction,
    the head moves in the specified direction by the given number of steps. The tail (and any
    intermediate knots) follow the head according to the move_tail function. Each time the tail moves,
    its position is recorded in a set to track unique positions visited.

    Args:
        instructions (list): A list of instructions where each instruction consists of a direction 
                              and a number of steps (e.g., "R 3").
        num_knots (int): The number of knots in the rope, including the head and tail.

    Returns:
        int: The total number of unique positions visited by the tail at least once.
    """
    # Start with the head at [0, 0] and all knots at [0, 0]
    knots = [[0, 0] for _ in range(num_knots)]
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

    # Process each instruction
    for instruction in instructions:
        direction, steps = instruction.split()
        steps = int(steps)
        
        # Move the head knot and then move the rest of the knots
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
