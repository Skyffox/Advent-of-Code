# pylint: disable=line-too-long
"""
Part 1: Two of the same antennas create an antinode that is in the position that extends from the two antennas, in both directions
        Find the amount of anitnodes that are still in the grid
Answer: 301

Part 2: Same as part 1, but the antinodes now propagate in both directions
Answer: 1019
"""

from utils import profiler


def within_grid(x: int, y: int, x_limit: int, y_limit: int) -> bool:
    """Check whether we still are in the grid"""
    return 0 <= x < x_limit and 0 <= y < y_limit


def get_input(file_path: str) -> list:
    """Get the input data"""
    grid = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            grid.append(list(line.strip()))

    return grid


def find_antennas(grid: list) -> dict:
    """Find all antennas and since there are different types, group the same ones together"""
    antennas = {}
    for y, row in enumerate(grid):
        for x, item in enumerate(row):
            if item != ".":
                if item not in antennas:
                    antennas[item] = [[y, x]]
                else:
                    # Create a list of lists for each position that this particular antenna appears in
                    antennas.update({item: antennas[item] + [[y, x]]})

    return antennas


@profiler
def antinodes(grid: list, antennas: dict, is_part2=False) -> int:
    """
    Find the difference in coordinates between similar antennas and fill the grid with antinodes
    for Part 2, we propagate further up and down the grid until we exit the grid
    """
    x_limit = len(grid[0])
    y_limit = len(grid)

    # Create an empty grid, in which we will store the antinodes. NOTE: We want to keep track of the
    # antennas with a grid because two antinodes (from different antenna) in the same position do not count for 2
    antinode_grid = [["."] * x_limit for _ in range(y_limit)]

    # Create the antinodes, iterate over the keys first
    for sort_antenna in antennas:
        # Loop twice over all locations and compare the first location with the rest
        # then the second location with the third and after etc...
        for idx, loc1 in enumerate(antennas[sort_antenna]):
            for loc2 in antennas[sort_antenna][idx+1:]:
                # Create the difference between the two antennas, 1 antinode for each antenna
                x_diff, y_diff = loc1[0] - loc2[0], loc1[1] - loc2[1]
                antinode_1x, antinode_1y = loc1[0] + x_diff, loc1[1] + y_diff
                antinode_2x, antinode_2y = loc2[0] - x_diff, loc2[1] - y_diff

                # If the antinode is within the grid, we have a valid antinode and we add it to the grid
                if within_grid(antinode_1x, antinode_1y, x_limit, y_limit):
                    antinode_grid[antinode_1x][antinode_1y] = "#"

                if within_grid(antinode_2x, antinode_2y, x_limit, y_limit):
                    antinode_grid[antinode_2x][antinode_2y] = "#"

                if is_part2:
                    # In Part 2, the antennas also count for antinodes in this part
                    antinode_grid[loc1[0]][loc1[1]] = "#"
                    antinode_grid[loc2[0]][loc2[1]] = "#"

                    # Propagate the difference further in both directions, keep creating antinodes untill we leave the grid
                    while within_grid(antinode_1x, antinode_1y, x_limit, y_limit):
                        antinode_grid[antinode_1x][antinode_1y] = "#"
                        antinode_1x, antinode_1y = antinode_1x + x_diff, antinode_1y + y_diff

                    while within_grid(antinode_2x, antinode_2y, x_limit, y_limit):
                        antinode_grid[antinode_2x][antinode_2y] = "#"
                        antinode_2x, antinode_2y = antinode_2x - x_diff, antinode_2y - y_diff

    # Count amount of # in the antinode grid
    return sum([row.count("#") for row in antinode_grid])


if __name__ == "__main__":
    # Get input data
    input_data = get_input("inputs/8_input.txt")
    antennae = find_antennas(input_data)

    print(f"Part 1: {antinodes(input_data, antennae)}")
    print(f"Part 2: {antinodes(input_data, antennae, True)}")
