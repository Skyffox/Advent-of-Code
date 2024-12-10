# pylint: disable=line-too-long
"""
Part 1: Find all the squares in a grid that have overlap between two or more claim ids
Answer: 118322

Part 2: Find the claim id that has no overlap
Answer: 1178
"""

from utils import profiler


def get_input(file_path: str) -> list:
    """Get the input data"""
    claims = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip().split()

            claim_id = line[0].split("#")[1]
            width_start = int(line[2].split(",")[0])
            height_start = int(line[2].split(",")[1].split(":")[0])
            width = int(line[3].split("x")[0])
            height = int(line[3].split("x")[1])

            claims.append([width_start, height_start, width, height, claim_id])

    return claims


@profiler
def part_1(claims: list) -> tuple[int, dict]:
    """Fill our dict for which squares a claim is in"""
    grid = {}
    for claim in claims:
        width_start, height_start, width, height, _ = claim

        # Add all squares to a grid and update ones we have already seen
        for x in range(width_start, width_start + width):
            for y in range(height_start, height_start + height):
                if (x, y) not in grid:
                    grid[(x, y)] = 1
                else:
                    grid[(x, y)] += 1

    return sum([1 for val in grid.values() if val > 1]), grid


@profiler
def part_2(claims: list, grid: dict) -> int:
    """Iterate over all claims again and see where there is no overlap"""
    for claim in claims:
        width_start, height_start, width, height, claim_id = claim
        overlap = False

        for x in range(width_start, width_start + width):
            for y in range(height_start, height_start + height):
                if grid[(x, y)] > 1:
                    overlap = True
        if not overlap:
            return claim_id


if __name__ == "__main__":
    input_data = get_input("inputs/3_input.txt")

    n, populated_grid = part_1(input_data)

    print(f"Part 1: {n}")
    print(f"Part 2: {part_2(input_data, populated_grid)}")
