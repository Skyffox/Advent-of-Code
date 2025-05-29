# pylint: disable=line-too-long
"""
Day 17: Reservoir Research

Part 1: How many tiles can the water reach within the range of y values in your scan?
Answer: 30384

Part 2: How many water tiles are left after the water spring stops producing water and all remaining water not at rest has drained?
Answer: 24479
"""

import re
import time


class Reservoir:
    """
    Represents a 2D grid simulating the flow of water through a cross-section of the ground.

    The grid includes sand ('.'), clay ('#'), and a water spring ('+'). Water flows downward
    when possible and spreads left and right, filling spaces that are blocked by clay on both sides.
    """
    def __init__(self, clay_positions):
        """
        Initialize the model with the clay positions.

        Args:
            clay_positions (set of (x,y) tuples): Positions of clay in the grid.
        """
        self.clay = clay_positions
        self.still = set()   # Positions with still water
        self.flowing = set() # Positions with flowing water

        self.min_x = min(x for x, y in self.clay)
        self.max_x = max(x for x, y in self.clay)
        self.min_y = min(y for x, y in self.clay)
        self.max_y = max(y for x, y in self.clay)

    def stop(self, x, y):
        """
        Return True if position (x, y) contains clay.

        Args:
            x (int): X-coordinate
            y (int): Y-coordinate

        Returns:
            bool: True if clay is at (x,y), else False.
        """
        return (x, y) in self.clay

    def pile(self, x, y):
        """
        Return True if position (x, y) contains clay or still water,
        i.e., water can pile up here.

        Args:
            x (int): X-coordinate
            y (int): Y-coordinate

        Returns:
            bool: True if clay or still water is at (x,y), else False.
        """
        return (x, y) in self.clay or (x, y) in self.still

    def simulate(self, start_x=500, start_y=0):
        """
        Run the water flow simulation starting at (start_x, start_y).

        The simulation uses an explicit stack to avoid recursion,
        performing 'fall' and 'scan' actions iteratively until stable.

        Args:
            start_x (int): Starting X position for water source.
            start_y (int): Starting Y position for water source.
        """
        stack = [('fall', start_x, start_y)]

        while stack:
            action, x, y = stack.pop()

            if action == 'fall':
                # Fall down until hitting pile (clay or still water)
                while y <= self.max_y and not self.pile(x, y + 1):
                    self.flowing.add((x, y))
                    y += 1
                if y <= self.max_y:
                    self.flowing.add((x, y))
                    # After falling, scan left and right on this row
                    stack.append(('scan', x, y))

            elif action == 'scan':
                # Scan left and right for boundaries and possible water spill
                min_x = x
                while self.pile(min_x, y + 1) and not self.stop(min_x - 1, y):
                    min_x -= 1
                max_x = x
                while self.pile(max_x, y + 1) and not self.stop(max_x + 1, y):
                    max_x += 1

                left_blocked = self.stop(min_x - 1, y)
                right_blocked = self.stop(max_x + 1, y)

                if left_blocked and right_blocked:
                    # Water is contained, convert flowing water to still
                    for xx in range(min_x, max_x + 1):
                        self.still.add((xx, y))
                        self.flowing.discard((xx, y))
                    # Water piles up, scan the row above
                    stack.append(('scan', x, y - 1))
                else:
                    # Water flows, mark current row as flowing
                    for xx in range(min_x, max_x + 1):
                        self.flowing.add((xx, y))
                    # If not blocked on sides, water falls off edges
                    if not left_blocked:
                        stack.append(('fall', min_x, y))
                    if not right_blocked:
                        stack.append(('fall', max_x, y))

    def count_all(self):
        """
        Count total water tiles (flowing + still) within vertical clay bounds.

        Returns:
            int: Number of water tiles between min and max clay y-coordinates.
        """
        return sum(1 for _, y in self.still | self.flowing if self.min_y <= y <= self.max_y)

    def count_still(self):
        """
        Count total still water tiles within vertical clay bounds.

        Returns:
            int: Number of still water tiles between min and max clay y-coordinates.
        """
        return sum(1 for _, y in self.still if self.min_y <= y <= self.max_y)


def get_input(file_path):
    """
    Parse input lines to extract clay positions.

    Args:
        lines (list of str): Lines of input describing clay veins.

    Returns:
        set of (x, y) tuples representing clay positions.
    """
    clay_positions = set()
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            a, b0, b1 = map(int, re.findall(r'\d+', line))
            if line[0] == 'x':
                for b in range(b0, b1 + 1):
                    clay_positions.add((a, b))
            else:
                for b in range(b0, b1 + 1):
                    clay_positions.add((b, a))
    return clay_positions


if __name__ == "__main__":
    clay = get_input("inputs/17_input.txt")
    model = Reservoir(clay)

    start_time = time.time()
    model.simulate()
    end_time = time.time()

    print(f"Execution time: {end_time - start_time:.4f} seconds")
    print(f"Part 1: {model.count_all()}")
    print(f"Part 2: {model.count_still()}")
