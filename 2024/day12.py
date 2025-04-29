# pylint: disable=line-too-long
"""
Part 1: What is the total price of fencing all regions on your map?
Answer: 1400386

Part 2: What is the new total price of fencing all regions on your map?
Answer: 851994
"""

from utils import profiler


def get_input(file_path: str) -> list:
    """Get the input data"""
    with open(file_path, "r", encoding="utf-8") as file:
        return [list(line.strip()) for line in file]


def is_valid(x: int, y: int, grid: list) -> bool:
    """Check if a cell is within bounds of the grid"""
    return 0 <= x < len(grid) and 0 <= y < len(grid[0])


def dfs(x: int, y: int, grid: list, visited: list, current_group: list) -> list:
    """Depth-First Search function to find connected letters that are the same"""
    # Define the directions for traversal (right, left, down, up)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Use pass by reference to know what positions we have visited
    visited[x][y] = True
    current_group.append((x, y))

    # Explore all 4 directions
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        # The letter we find needs to be in the grid, the same as our original letter and also a unique position
        if is_valid(nx, ny, grid) and grid[nx][ny] == grid[x][y] and not visited[nx][ny]:
            dfs(nx, ny, grid, visited, current_group)


def find_groups(grid: list) -> list:
    """Find groups of the same letter"""
    visited = [[False for _ in range(len(grid[0]))] for _ in range(len(grid))]
    groups = []

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if not visited[i][j]:
                current_group = []
                dfs(i, j, grid, visited, current_group)
                if current_group:
                    groups.append(current_group)

    return groups


def find_consecutive_positions(positions: list, check_vertical=False) -> list:
    """Find sequences of the same value for a given coordinate"""
    # Sort the positions first by x-coordinate (row) and then by y-coordinate (column)
    sorted_positions = sorted(positions)
    x, y = 0, 1

    if check_vertical:
        # Find vertical sequences (same column, consecutive rows)
        sorted_positions = sorted(positions, key=lambda x: (x[1], x[0]))
        x, y = y, x

    groups = []

    current_group = []
    for idx, pos in enumerate(sorted_positions):
        if not current_group:
            current_group.append(pos)
        else:
            if pos[x] == sorted_positions[idx-1][x] and pos[y] == sorted_positions[idx-1][y] + 1:
                current_group.append(pos)
            else:
                if len(current_group) > 1:
                    groups.append(current_group)
                current_group = [pos]

    if len(current_group) > 1:
        groups.append(current_group)

    return groups


@profiler
def part_one(grid: list) -> int:
    """Find the parameter of all the groups in the grid, so the elves know how much metres of fence to buy"""
    groups = find_groups(grid)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    perimeter = 0
    for group in groups:
        if len(group) == 1:
            p = 4
        else:
            # Maximum perimeter for a group is the amount of tiles in the group times 4 (one for each side)
            p = len(group) * 4

            for x, y in group:
                # Now find all the overlap between the tiles because we don't need fences between members from the same group
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if (nx, ny) in group:
                        p -= 1

        perimeter += len(group) * p

    return perimeter


@profiler
def part_two(grid: list) -> int:
    """Instead of counting tiles we now need to count the unique amount of sides for an area"""
    groups = find_groups(grid)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    perimeter = 0
    for group in groups:
        total_sides = 0

        if len(group) == 1:
            total_sides = 4
        else:
            # First find all the horizontal and vertical groups within our area, then we will iterate over these groups
            horizontal = find_consecutive_positions(group)
            vertical = find_consecutive_positions(group, True)
            total_visited_fences = []

            for row in horizontal:
                visited_fences = []

                for y, x in row:
                    number = grid[y][x]
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        valid = is_valid(nx, ny, grid)
                        # Add a fence when our number from the current position is different from our original
                        # We may place fences outside the grid because we place them in positions around the current position
                        if (valid and grid[ny][nx] != number) or not valid:
                            visited_fences.append((ny, nx))

                # Now we have all fences for a particular group, but we still need to know how many of these fences form a side
                horizontal_sides = find_consecutive_positions(visited_fences)
                total_sides += len(horizontal_sides)
                # Add all these positions to the visited list, since they now have a fence
                total_visited_fences.extend([x for xs in horizontal_sides for x in xs])

            for col in vertical:
                visited_fences = []

                for y, x in col:
                    number = grid[y][x]
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        valid = is_valid(nx, ny, grid)
                        # Add a fence when our number from the current position is different from our original
                        # We may play fences outside the grid because we place them in positions around the current position
                        if (valid and grid[ny][nx] != number) or not valid:
                            visited_fences.append((ny, nx))

                # Now we have all fences for a particular group, but we still need to know how many of these fences form a side
                vertical_sides = find_consecutive_positions(visited_fences, True)
                total_sides += len(vertical_sides)
                # Add all these positions to the visited list, since they now have a fence
                total_visited_fences.extend([x for xs in vertical_sides for x in xs])

            # There are some positions that are not part of a side, here we will add the fences for these positions
            for x, y in group:
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    # We have a fence for this position already
                    if (nx, ny) in total_visited_fences:
                        total_visited_fences.remove((nx, ny))
                    else:
                        if (nx, ny) not in group:
                            total_sides += 1

        # The perimeter is the surface area of the group times the amount of sides that require a fence
        perimeter += len(group) * total_sides

    return perimeter


if __name__ == "__main__":
    # Get input data
    input_data = get_input("inputs/12_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
