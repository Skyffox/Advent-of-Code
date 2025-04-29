# pylint: disable=line-too-long
"""
Part 1: 
Answer: 370

Part 2: 
Answer: 363
"""

from utils import profiler


def get_input(file_name):
    """Read the grid and locate 'S' (source) and 'E' (target)"""
    grid = []
    source, target = None, None
    with open(file_name, "r", encoding="utf-8") as file:
        for i, line in enumerate(file):
            row = []
            for j, char in enumerate(line.strip()):
                # 'S' is treated as elevation 0
                if char == 'S':
                    source = (j, i)
                    row.append(0)
                # 'E' is treated as elevation 25
                elif char == 'E':
                    target = (j, i)
                    row.append(25)
                # Convert letter to elevation (0 for 'a', 25 for 'z')
                else:
                    row.append(ord(char) - ord('a'))

            grid.append(row)

    return grid, source, target


def validate_move(grid, x, y, elevation):
    '''returns True if the coordinates are inside the grid and the climb is not too steep'''
    x_range, y_range = range(len(grid[0])), range(len(grid))
    return (x in x_range) and (y in y_range) and (grid[y][x] < elevation + 2)


def navigate(grid, source, target):
    """"a"""
    steps = elevation = 0
    visited = {(source): (steps, elevation)}
    queue = [(source)]

    while queue:
        x, y = queue.pop(0)
        steps, elevation = visited[(x, y)]

        if x == target[0] and y == target[1]:
            return steps if queue else float("inf")

        moves = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        possible_moves = [(x, y) for x, y in moves if validate_move(grid, x, y, elevation)]

        for x, y in possible_moves:
            if (x, y) not in visited:
                visited[(x, y)] = (steps + 1, grid[y][x])
                queue.append((x, y))


@profiler
def part_1(grid, source, target):
    """a"""    
    return navigate(grid, source, target)


@profiler
def part_2(grid, target):
    """g"""
    possible_starts = [(x, y) for y, row in enumerate(grid) for x, elevation in enumerate(row) if elevation == 0]
    return min(filter(lambda x: x is not None, [navigate(grid, source, target) for source in possible_starts]))


if __name__ == "__main__":
    elevations, start, end = get_input("inputs/12_input.txt")

    print(part_1(elevations, start, end))
    print(part_2(elevations, end))
