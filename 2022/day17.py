# pylint: disable=line-too-long
"""
Part 1: How many units tall will the tower of rocks be after 2022 rocks have stopped falling?
Answer: 3239

Part 2: How tall will the tower be after 1000000000000 rocks have stopped?
Answer: 1594842406882
"""

from utils import profiler


def get_input(file_path: str) -> list:
    """Get the input data"""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.readlines()[0]


def new_rock(h: int, n: int) -> list:
    """
    Return a rock with a certain form and place it two spaces to the right and three places up, 
    otherwise it might collide with the biggest rock (Vertical line)
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


def can_place_rock(rock: tuple[int, int], columns: dict) -> bool:
    """Check whether new position collides with wall or another rock, does a check for horizontal movement and vertical"""
    for x, y in rock:
        if y < 0 or x < 0 or x >= 7 or y in columns[x]:
            return False
    return True


def update_pos(column: dict[set], rock: list) -> dict:
    """Update the positions in the column with the latest position of a rock"""
    for coord in rock:
        rx, ry = coord
        column[rx].add(ry)
    return column


@profiler
def simulate_rock_fall(jet_pattern, total_rocks):
    """Simulate the falling of num_rocks based on the jet_pattern"""
    columns = {
        # key (0-7) is the column index. value is a set of occupied y coordinates
        0: set(),
        1: set(),
        2: set(),
        3: set(),
        4: set(),
        5: set(),
        6: set()
    }

    jet_index = 0
    height = 0
    rock_count = 0
    temp_rock = (0, 0)

    # Part 2 variables
    states = {}
    cycle_found = False
    height_increase = 0

    # Simulate the falling of rocks
    while rock_count < total_rocks:
        # Start by placing the rock at the top of the column. Repeat the rock shapes in cycle
        rock = new_rock(height, rock_count % 5)

        # Apply gas jets and move the rock down
        while True:
            # Move the rock horizontally based on the jet pattern
            jet_move = jet_pattern[jet_index % len(jet_pattern)]
            jet_index += 1

            # Move left or right based on the jet move
            if jet_move == ">":
                temp_rock = [(x + 1, y) for x, y in rock]
            elif jet_move == "<":
                temp_rock = [(x - 1, y) for x, y in rock]

            # If we can move horizontally, do so
            if can_place_rock(temp_rock, columns):
                rock = temp_rock

            # Move the rock downward (fall)
            temp_rock = [(x, y - 1) for x, y in rock]
            if can_place_rock(temp_rock, columns):
                rock = temp_rock
            else:
                # Rock is at rest
                break

        # Update columns with rock's final position
        columns = update_pos(columns, rock)
        height = max((max(col) for _, col in columns.items() if col), default=0) + 1

        # Part 2 stuff to check for states!
        if not cycle_found:
            # Get the maximum height of each column
            max_cols = [max(max(col) for _, col in columns.items() if col)]

            # Adjust the maximum heights so that they are relative to each other
            # so the lowest one will be zero (or -1 for the floor) and the others will
            # be the difference between their height and the lowest.
            min_col = min(max_cols)
            relative_cols = [mc - min_col for mc in max_cols]

            # Add the rock order (so what tetris shape this is) and the jet index to the state
            curr_state = relative_cols.extend([rock_count % 5, jet_index % len(jet_pattern)])
            curr_state = tuple(relative_cols)

            if curr_state in states:
                # Cycle found! Now we find the various attributes of the cycle
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
