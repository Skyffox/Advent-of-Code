# pylint: disable=line-too-long
"""
Part 1: In the row where y=2000000, how many positions cannot contain a beacon?
Answer: 6078701

Part 2: Find the only possible position for the distress beacon. What is its tuning frequency?
Answer: 12567351400528
"""

from utils import profiler


def get_input(file_path: str) -> list:
    """Get the input data"""
    data = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip().split("=")

            sensor = [int(line[1].split(",")[0]), int(line[2].split(":")[0])]
            beacon = [int(line[3].split(",")[0]), int(line[4].split(":")[0])]

            # Manhattan distance: is the sum of the lengths of the projections of the line segment between the points onto the coordinate axes.
            manhattan_distance = abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])

            data.append(((sensor), manhattan_distance))

    return data


def seen_in_row(sensors, row):
    """Get all edges that are outside the range of the sensor"""
    all_edges = []
    for (sx, sy), dist in sensors:
        diff = dist - abs(row - sy)
        if diff >= 0:
            all_edges.append((sx-diff, sx+diff))

    return sorted(all_edges)


def find_a_hole(edges):
    """
    The edges are a list with each entry having a low and high point. 
    Sorting these low and high points makes them form a continuous range. 
    This function checks a what point the range is not continuous anymore
    """
    highest = 0
    for (a, b) in edges:
        if a <= highest + 1:
            highest = max(b, highest)
        else:
            return a - 1


@profiler
def part_1(data):
    """See if range crosses the line and add coordinates"""
    limit = 2000000
    x_coors = set()

    for (sx, sy), dist in data:
        # Check if target is within vertical range of the sensor
        diff =  dist - abs(limit - sy)
        if diff >= 0:
            # These are all positions a beacon can not be placed
            for i in range(-diff, diff + 1):
                x = sx + i
                x_coors.add(x)

    return len(x_coors) - 1


@profiler
def part_2(sensors: list):
    """Find the only possible position for the distress beacon"""
    limit = 4000000

    for row in reversed(range(limit + 1)):
        edges = seen_in_row(sensors, row)
        # Assign value to col as part of an expression
        if col := find_a_hole(edges):
            # Formula for the beacons tuning signal
            return limit * col + row


if __name__ == "__main__":
    input_data = get_input("inputs/15_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
