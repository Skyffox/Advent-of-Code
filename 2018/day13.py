# pylint: disable=line-too-long
"""
Day 13: Mine Cart Madness

Part 1: Find the location of the first crash.
Answer: 118,112

Part 2: Find the location of the last cart after all collisions.
Answer: 50,21
"""

from typing import Dict, List, Tuple
from utils import profiler


DIRS = {
    '^': (0, -1),
    'v': (0, 1),
    '<': (-1, 0),
    '>': (1, 0)
}

STRAIGHT = {
    (0, -1): (0, -1),
    (0, 1): (0, 1),
    (-1, 0): (-1, 0),
    (1, 0): (1, 0)
}


LEFT_TURN = {
    (0, -1): (-1, 0),  # ^ to <
    (0, 1): (1, 0),    # v to >
    (-1, 0): (0, 1),   # < to v
    (1, 0): (0, -1)    # > to ^
}

RIGHT_TURN = {
    (0, -1): (1, 0),   # ^ to >
    (0, 1): (-1, 0),   # v to <
    (-1, 0): (0, -1),  # < to ^
    (1, 0): (0, 1)     # > to v
}

FORWARD_SLASH_TURN = {
    (0, -1): (1, 0),   # ^ to >
    (0, 1): (-1, 0),   # v to <
    (-1, 0): (0, 1),   # < to v
    (1, 0): (0, -1)    # > to ^
}

BACK_SLASH_TURN = {
    (0, -1): (-1, 0),  # ^ to <
    (0, 1): (1, 0),    # v to >
    (-1, 0): (0, -1),  # < to ^
    (1, 0): (0, 1)     # > to v
}

TURN_CYCLE = [LEFT_TURN, STRAIGHT, RIGHT_TURN]


class Cart:
    """
    Represents a cart moving on a 2D track grid.

    Attributes:
        p (Tuple[int, int]): Current position of the cart as (x, y).
        d (Tuple[int, int]): Current direction vector of the cart.
        i (int): Index used to determine the next turn at intersections (cycles through 0: left, 1: straight, 2: right).
        collided (bool): Flag indicating if the cart is still active (not involved in a crash).
    """

    def __init__(self, position: Tuple[int, int], direction: Tuple[int, int]):
        """
        Initializes a new Cart object.

        Args:
            position (Tuple[int, int]): Initial position of the cart (x, y).
            direction (Tuple[int, int]): Initial direction vector (dx, dy).
        """
        self.p = position
        self.d = direction
        self.i = 0
        self.collided = True

    def step(self, grid: Dict[Tuple[int, int], str]) -> None:
        """
        Moves the cart one step in its current direction, and updates its direction
        based on the type of track it encounters.

        Args:
            grid (Dict[Tuple[int, int], str]): The track grid mapping positions to track characters.
        """
        self.p = (self.p[0] + self.d[0], self.p[1] + self.d[1])
        track_piece = grid[self.p]

        if track_piece == '+':
            # Handle intersection
            self.d = TURN_CYCLE[self.i % 3][self.d]
            self.i += 1
        elif track_piece == '/':
            self.d = FORWARD_SLASH_TURN[self.d]
        elif track_piece == '\\':
            self.d = BACK_SLASH_TURN[self.d]

    def hits(self, other: 'Cart') -> bool:
        """
        Checks whether this cart has collided with another cart.

        Args:
            other (Cart): Another cart to compare against.

        Returns:
            bool: True if both carts are active and occupy the same position; False otherwise.
        """
        return self != other and self.collided and other.collided and self.p == other.p


def get_input(file_path: str) -> Tuple[Dict[Tuple[int, int], str], List[Cart]]:
    """
    Parses the input file to create a grid and initialize all carts.

    Args:
        file_path (str): Path to the input file.

    Returns:
        Tuple[Dict[Tuple[int, int], str], List[Cart]]: Track grid and list of carts.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        lines = [list(line.rstrip('\n')) for line in file]

    grid = {}
    carts = []

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            pos = (x, y)
            if char in DIRS:
                carts.append(Cart(pos, DIRS[char]))
                grid[pos] = '-' if char in '<>' else '|'
            else:
                grid[pos] = char

    return grid, carts


@profiler
def compute(grid: Dict[Tuple[int, int], str], carts: List[Cart], is_part2: bool) -> str:
    """
    Runs the cart simulation.

    Args:
        grid: The track layout.
        carts: List of cart objects.
        is_part2: Whether to run part 2 logic (remove crashed carts).

    Returns:
        str: The crash or last cart's position as 'x,y'.
    """
    while True:
        # Sort carts in top-to-bottom, left-to-right order
        carts.sort(key=lambda c: (c.p[1], c.p[0]))

        for cart in carts:
            if not cart.collided:
                continue

            cart.step(grid)

            for other in carts:
                if cart.hits(other):
                    cart.collided = other.collided = False
                    if not is_part2:
                        return f"{cart.p[0]},{cart.p[1]}"

        # Filter out crashed carts
        carts = [c for c in carts if c.collided]

        if is_part2 and len(carts) == 1:
            return f"{carts[0].p[0]},{carts[0].p[1]}"


if __name__ == "__main__":
    track, objects = get_input("inputs/13_input.txt")

    print(f"Part 1: {compute(track, list(objects), False)}")
    print(f"Part 2: {compute(track, list(objects), True)}")
