# Part 1: In the row where y=2000000, how many positions cannot contain a beacon?
# Answer: 6078701

# Part 2: Find the only possible position for the distress beacon. What is its tuning frequency?
# Answer: 12567351400528

# See if range crosses the line and add coordinates
def find(data, limit):
    x_coors = set()
    for (sx, sy), r in data:
            diff =  r - abs(limit - sy)
            if diff >= 0:
                for i in range(-diff, diff + 1):
                    x = sx + i
                    x_coors.add(x)
    return x_coors


def seen_in_row(sensors, row):
    all_edges = []
    for (sx, sy), r in sensors:
        diff =  r - abs(row - sy)
        if diff >= 0:
            all_edges.append((sx-diff, sx+diff))
    return sorted(all_edges)


def find_a_hole(edges):
    highest = 0
    for (a, b) in edges:
        if a <= highest + 1:
            highest = max(b, highest)
        else:
            return a - 1


def part_2(sensors, limit):
    for row in reversed(range(limit + 1)):
        edges = seen_in_row(sensors, row)
        if col := find_a_hole(edges):
            return limit * col + row


data = []
with open("inputs/15_input.txt") as f:
    for line in f:
        line = line.strip().split("=")

        sensor = [int(line[1].split(",")[0]), int(line[2].split(":")[0])]
        beacon = [int(line[3].split(",")[0]), int(line[4].split(":")[0])]

        # Manhattan distance: is the sum of the lengths of the projections of the line segment between the points onto the coordinate axes.
        manhattan_distance = abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])

        data.append(((sensor[0], sensor[1]), manhattan_distance))


limit = 4000000
print("Number of positions without beacon:", len(find(data, limit // 2)) - 1)
print("Tuning frequency:", part_2(data, limit))