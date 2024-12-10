# pylint: disable=line-too-long
"""
Part 1: How much wrapping paper is needed for a present with certain dimensions
Answer: 1588178

Part 2: The elves want a ribbon to wrap the present, calculate how much feet they need
Answer: 3783758
"""

from utils import profiler


def get_input(file_path: str) -> tuple[list, list, list]:
    """Get the input data"""
    width, length, height = [], [], []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = list(map(int, line.strip().split("x")))
            width.append(line[0])
            length.append(line[1])
            height.append(line[2])

    return width, length, height


@profiler
def part_1(width: list, length: list, height: list) -> int:
    """Find the surface area for the amount of wrapping paper we need"""
    total = 0
    for idx, _ in enumerate(width):
        side_1 = length[idx] * width[idx]
        side_2 = width[idx] * height[idx]
        side_3 = height[idx] * length[idx]
        smallest_side = min(side_1, side_2, side_3)

        total += 2 * side_1 + 2 * side_2 + 2 * side_3 + smallest_side

    return total


@profiler
def part_2(width: list, length: list, height: list) -> int:
    """
    The ribbon required to wrap a present is the shortest distance around its sides, 
    or the smallest perimeter of any one face
    """
    total = 0
    for idx, _ in enumerate(width):
        bow = width[idx] * length[idx] * height[idx]
        biggest_side = max(width[idx], length[idx], height[idx])

        ribbon = 0
        if width[idx] == biggest_side:
            ribbon = 2 * length[idx] + 2 * height[idx]
        elif length[idx] == biggest_side:
            ribbon = 2 * width[idx] + 2 * height[idx]
        else:
            ribbon = 2 * width[idx] + 2 * length[idx]

        total += ribbon + bow

    return total


if __name__ == "__main__":
    w, l, h = get_input("inputs/2_input.txt")

    print(f"Part 1: {part_1(w, l, h)}")
    print(f"Part 2: {part_2(w, l, h)}")
