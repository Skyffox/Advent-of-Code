# pylint: disable=line-too-long
"""
Part 1: Find all numeric values that are adjacent to a symbol (not the dot)
Answer: 554003

Part 2: Find the numeric values of which there are TWO adjacent to the * symbol
Answer: 87263515
"""

from utils import profiler


def get_input(file_path: str) -> list:
    """Get the input data"""
    with open(file_path, "r", encoding="utf-8") as file:
        return [list(line.strip()) for line in file]


def check_value(y: int, x: int, grid: list) -> tuple[bool, set]:
    """Search around a coordinate in the grid to see if we find a special symbol"""
    asterisk_coor = ()
    for y_offset in range(-1, 2):
        for x_offset in range(-1, 2):
            # Search in a 3x3 grid around the coordinate for a symbol.
            if y + y_offset > len(grid) - 1 or y + y_offset < 0 or x + x_offset > len(grid[0]) - 1 or x + x_offset < 0:
                continue

            val = grid[y + y_offset][x + x_offset]
            if not val.isdigit() and not val == '.':
                # Add the coordinate of the asterisk in the return value.
                if val == "*":
                    asterisk_coor = (y + y_offset, x + x_offset)

                return True, (y + y_offset, x + x_offset)
    return False, asterisk_coor


@profiler
def part_1(grid: list) -> int:
    """Find the full number with its coordinates then check for each coordinate whether its adjacent to an asterisk"""
    number_coords = []
    n = 0
    for y, line in enumerate(grid):
        sublst = []
        for x, val in enumerate(line):
            # We want to locate the full number with its coordinates in the grid so we can loop over the coordinates later.
            if val.isdigit():
                sublst.append([str(val), (y, x)])

                # Add number and coords to list when a non numeric value was found.
                if x == len(line) - 1 or not line[x + 1].isdigit():
                    num = int(''.join([item[0] for item in sublst]))
                    coords = [item[1] for item in sublst]
                    number_coords.append((num, coords))
                    sublst = []

    # Check how many full numbers are not adjacent to an asterisk
    for num, coords in number_coords:
        for coor in coords:
            valid = check_value(coor[0], coor[1], grid)
            if valid[0]:
                n += num
                break

    return n, number_coords


@profiler
def part_2(lst: list, grid: list) -> int:
    """
    Find all gears (* symbol) in the grid and find the gear ratio. 
    That is if there are exactly two numbers adjacent to a gear then multiply them together
    """
    gear_ratio = 0
    asterisks = {}
    for num, coords in lst:
        for coor in coords:
            valid = check_value(coor[0], coor[1], grid)
            # See if number is adjacent to asterisk
            if valid[1]:
                if valid[1] not in asterisks:
                    # Add new asterisk coordinate
                    asterisks.update({valid[1] : [num]})
                else:
                    # Add number coordinate to existing asterisk.
                    asterisks[valid[1]].append(num)
            if valid[0]:
                break

    # For all asterisks with two adjacent numeric values add the product of the two numbers.
    for _, value in asterisks.items():
        if len(value) == 2:
            gear_ratio += (value[0] * value[1])

    return gear_ratio


if __name__ == "__main__":
    input_data = get_input("inputs/3_input.txt")

    total, coordinate_lst = part_1(input_data)

    print(f"Part 1: {total}")
    print(f"Part 2: {part_2(coordinate_lst, input_data)}")
