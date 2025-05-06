# pylint: disable=line-too-long
"""
Day 17: Pyroclastic Flow

Part 1: How many units tall will the tower of rocks be after 2022 rocks have stopped falling?
Answer: 3239

Part 2: How tall will the tower be after 1000000000000 rocks have stopped?
Answer: 1594842406882
"""

from collections import defaultdict
from utils import profiler


def get_input(file_path: str) -> str:
    """
    Read the jet pattern input from a file.

    Args:
        file_path (str): Path to the input file.

    Returns:
        str: A single-line string representing the jet pattern sequence ('<' or '>').
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return file.readlines()[0]


def new_rock(h: int, n: int) -> list:
    """
    Generate a new rock shape positioned at a height `h`, based on the rock index.

    Args:
        h (int): Current height of the tower.
        n (int): Rock index (0-4), determines shape.

    Returns:
        list: A list of (x, y) coordinate tuples representing the rock's blocks.
    """
    if n == 0:   # Horizontal line
        return [(2, h + 3), (3, h + 3), (4, h + 3), (5, h + 3)]
    elif n == 1: # Plus
        return [(2, h + 4), (3, h + 4), (4, h + 4), (3, h + 5), (3, h + 3)]
    elif n == 2: # L-shape
        return [(2, h + 3), (3, h + 3), (4, h + 3), (4, h + 4), (4, h + 5)]
    elif n == 3: # Vertical line
        return [(2, h + 3), (2, h + 4), (2, h + 5), (2, h + 6)]
    elif n == 4: # Square block
        return [(2, h + 3), (3, h + 3), (2, h + 4), (3, h + 4)]


def can_place_rock(rock: list, columns: defaultdict) -> bool:
    """
    Determine if the given rock can be placed at the current position.

    Args:
        rock (list): List of (x, y) coordinates representing the rock.
        columns (defaultdict): Map of column indices to sets of occupied y-values.

    Returns:
        bool: True if the rock can be placed (no collisions or boundary violations), else False.
    """
    for x, y in rock:
        if y < 0 or x < 0 or x >= 7 or y in columns[x]:
            return False
    return True


def update_pos(columns: defaultdict, rock: list) -> defaultdict:
    """
    Update the tower structure with the new rock's final position.

    Args:
        columns (defaultdict): Current column height map.
        rock (list): List of (x, y) positions of the placed rock.

    Returns:
        defaultdict: Updated column height map.
    """
    for x, y in rock:
        columns[x].add(y)
    return columns


@profiler
def simulate_rock_fall(jet_pattern: str, total_rocks: int) -> int:
    """
    Simulate falling rocks under the influence of a jet pattern and calculate final tower height.

    This function supports both Part 1 (2022 rocks) and Part 2 (1 trillion rocks) by detecting cycles
    in rock behavior and fast-forwarding through repeating patterns to optimize performance.

    Args:
        jet_pattern (str): Sequence of '<' and '>' characters that move rocks left or right.
        total_rocks (int): Total number of rocks to simulate.

    Returns:
        int: Final height of the tower after all rocks have been placed.
    """
    columns = defaultdict(set) # Using defaultdict for easier set management
    jet_index = 0
    height = 0
    rock_count = 0

    # Part 2 variables
    states = {}
    cycle_found = False
    height_increase = 0

    while rock_count < total_rocks:
        # Start by placing the rock at the top of the column. Repeat the rock shapes in cycle
        rock = new_rock(height, rock_count % 5)

        while True:
            # Apply jet pattern to move the rock horizontally
            jet_move = jet_pattern[jet_index % len(jet_pattern)]
            jet_index += 1
            temp_rock = [(x + 1, y) if jet_move == ">" else (x - 1, y) for x, y in rock]

            if can_place_rock(temp_rock, columns):
                rock = temp_rock

            # Move rock downward
            temp_rock = [(x, y - 1) for x, y in rock]
            if can_place_rock(temp_rock, columns):
                rock = temp_rock
            else:
                break # The rock has landed

        # Update columns with the rock's final position
        columns = update_pos(columns, rock)
        height = max((max(col) for col in columns.values() if col), default=0) + 1

        # Part 2: Detect cycle patterns
        if not cycle_found:
            # Get the maximum height of each column
            max_cols = [max(col) for col in columns.values() if col]

            # Adjust the maximum heights so that they are relative to each other
            # so the lowest one will be zero (or -1 for the floor) and the others will
            # be the difference between their height and the lowest.
            min_col = min(max_cols)
            relative_cols = tuple(mc - min_col for mc in max_cols)
            # Add the rock order (so what tetris shape this is) and the jet index to the state
            curr_state = relative_cols + (rock_count % 5, jet_index % len(jet_pattern))

            if curr_state in states:
                cycle_found = True
                rocks_per_cycle = rock_count - states[curr_state]['rock']
                height_per_cycle = height - states[curr_state]['height']
                remaining_rocks = total_rocks - rock_count
                cycles_remaining = remaining_rocks // rocks_per_cycle
                rock_remainder = remaining_rocks % rocks_per_cycle
                
                # We have some rocks left to simulate (the remainder) so we calculate the height
                # increase after all the cycles are done, and set the rock_count so that
                # we only have the rock_remainder left to simulate
                height_increase = height_per_cycle * cycles_remaining
                rock_count = total_rocks - rock_remainder
            else:
                states[curr_state] = {'rock': rock_count, 'height': height}

        rock_count += 1

    return height + height_increase


if __name__ == "__main__":
    input_data = get_input("inputs/17_input.txt")

    print(f"Part 1: {simulate_rock_fall(input_data, 2022)}")
    print(f"Part 2: {simulate_rock_fall(input_data, 1_000_000_000_000)}")
