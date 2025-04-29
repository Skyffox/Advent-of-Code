# pylint: disable=line-too-long
"""
Part 1: How many units of sand come to rest before sand starts flowing into the abyss below?
Answer: 728

Part 2: Using your scan, simulate the falling sand until the source of the sand becomes blocked. How many units of sand come to rest?
Answer: 27623
"""

from utils import profiler


def get_input(file_path: str) -> list:
    """Get the input data"""
    walls = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip().split(" -> ")
            line = [list(map(int, x.split(","))) for x in line]

            for idx, (x, y) in enumerate(line):
                walls.append([x, y])
                if idx == len(line) - 1:
                    break

                # Find all the walls, input is as follows: 498,4 -> 498,6 -> 496,6
                # A line is drawn between these points, that is where the walls are
                next_point = line[idx + 1]
                diff = abs(x - next_point[0]) if x != next_point[0] else abs(y - next_point[1])
                for d in range(1, diff):
                    # Check whether the difference is between the x or y coordinate
                    if x != next_point[0]:
                        # Check whether the line goes left or right
                        walls.append([x + (d if x < next_point[0] else -d), y])
                    else:
                        walls.append([x, y + (d if y < next_point[1] else -d)])

    return walls


def draw_canvas(walls, min_x, max_x, max_y):
    """DRAW: rock as #, air as ., and the source of the sand as +"""
    canvas = []
    for y in range(max_y + 1):
        canvas_line = []
        for pos_x in range(min_x, max_x + 1):
            if [pos_x, y] in walls:
                canvas_line.append("# ")
            # Position where the sand flows from
            elif [pos_x, y] == [500, 0]:
                canvas_line.append("+ ")
            else:
                canvas_line.append(". ")
        canvas.append(canvas_line)

    return canvas


def sand_propagation(canvas: list, sand_start: tuple[int, int], min_x: int) -> bool:
    """Sand particles move down if possible otherwise check either direction if there is an air tile"""
    y = sand_start[1]
    x = sand_start[0] - min_x

    while True:
        if y > len(canvas) - 2 or x < 0 or x > len(canvas[0]) - 1:
            return True

        # Check in which direction the sand can move
        if canvas[y+1][x] == ". ":
            y += 1
        elif canvas[y+1][x-1] == ". ":
            x -= 1
            y += 1
        elif canvas[y+1][x+1] == ". ":
            x += 1
            y += 1
        else:
            if canvas[y][x] == "+ ":
                return True

            canvas[y][x] = "* "
            return False


@profiler
def part_1(walls: list) -> int:
    """a"""
    overflow_count = 0

    min_x = min([x[0] for x in walls])
    max_x = max([x[0] for x in walls])
    max_y = max([x[1] for x in walls])

    canvas = draw_canvas(walls, min_x, max_x, max_y)

    while True:
        overflow_count += 1
        if sand_propagation(canvas, [500, 0], min_x):
            return overflow_count - 1


@profiler
def part_2(walls: list) -> int:
    """a"""
    overflow_count = 0

    min_x = min([x[0] for x in walls])
    max_x = max([x[0] for x in walls])
    max_y = max([x[1] for x in walls])

    min_x -= 200
    max_x += 200

    canvas = draw_canvas(walls, min_x, max_x, max_y)

    canvas.append([". " for _ in range(min_x, max_x + 1)])
    canvas.append(["# " for _ in range(min_x, max_x + 1)])

    while True:
        overflow_count += 1
        if sand_propagation(canvas, [500, 0], min_x):
            return overflow_count


if __name__ == "__main__":
    input_data = get_input("inputs/14_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
