# pylint: disable=line-too-long
"""
Part 1: 
Answer: 

Part 2: 
Answer: 
"""

from utils import profiler


def get_input(file_path: str) -> list:
    """Get the input data"""
    lst = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            lst.append([ch for ch in line.strip()])

    return lst


# Function to check if a cell is within bounds of the grid
def is_valid(x, y, grid, visited):
    return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and not visited[x][y]


# DFS function to find connected letters that are the same
def dfs(x, y, grid, visited, current_group, letter):
    # Define the directions for traversal (right, left, down, up)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    visited[x][y] = True
    current_group.append((x, y))  # Store the position (x, y)
    
    # Explore all 4 directions
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if is_valid(nx, ny, grid, visited) and grid[nx][ny] == letter:
            dfs(nx, ny, grid, visited, current_group, letter)


# Main function to find groups of the same letter
def find_groups(grid):
    rows = len(grid)
    cols = len(grid[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    groups = []
    
    for i in range(rows):
        for j in range(cols):
            if not visited[i][j]:
                current_group = []
                letter = grid[i][j]
                dfs(i, j, grid, visited, current_group, letter)
                if current_group:
                    groups.append(current_group)
    
    return groups


def find_consecutive_positions(positions):
    # Sort the positions first by x-coordinate (row) and then by y-coordinate (column)
    sorted_positions = sorted(positions)
    
    horizontal_groups = []
    vertical_groups = []
    
    # Find horizontal sequences (same row, consecutive columns)
    current_group = []
    for i in range(len(sorted_positions)):
        if not current_group:
            current_group.append(sorted_positions[i])
        else:
            if sorted_positions[i][0] == sorted_positions[i-1][0] and sorted_positions[i][1] == sorted_positions[i-1][1] + 1:
                current_group.append(sorted_positions[i])
            else:
                if len(current_group) > 1:
                    horizontal_groups.append(current_group)
                current_group = [sorted_positions[i]]
    if len(current_group) > 1:
        horizontal_groups.append(current_group)

    # Find vertical sequences (same column, consecutive rows)
    sorted_by_column = sorted(positions, key=lambda x: (x[1], x[0]))  # Sort by column (y), then by row (x)
    
    current_group = []
    for i in range(len(sorted_by_column)):
        if not current_group:
            current_group.append(sorted_by_column[i])
        else:
            if sorted_by_column[i][1] == sorted_by_column[i-1][1] and sorted_by_column[i][0] == sorted_by_column[i-1][0] + 1:
                current_group.append(sorted_by_column[i])
            else:
                if len(current_group) > 1:
                    vertical_groups.append(current_group)
                current_group = [sorted_by_column[i]]
    if len(current_group) > 1:
        vertical_groups.append(current_group)
    
    return horizontal_groups, vertical_groups


@profiler
def part_one(grid):
    """Comment"""
    # Call the function to find groups
    groups = find_groups(grid)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # find the perimeter for each group
    perimeter, p2 = 0, 0
    for group in groups:
        total_sides = 0

        # visited_fences = []
        if len(group) == 1:
            p = 4
            total_sides = 4
        else:
            # perimeter = area * # of fences
            p = len(group) * 4

            for pos in group:
                x, y = pos
                # add fences in all directions
                # visited_fences.extend([(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)])

                # Now find all the overlap between the positions because we dont need fences between the same
                # Explore all 4 directions
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if (nx, ny) in group:
                        p -= 1
                        # visited_fences.remove((nx, ny))

            # PART 2
            # we first get the horizontal and vertical groups within our group, then we see whether a side on this horizotna/vertical group is ondoorbroken
            # dan kunnen we het tellen als een "side" 
            horizontal, vertical = find_consecutive_positions(group)
            total_visited_fences = []
            for row in horizontal:
                visited_fences = []

                for pos in row:
                    y, x = pos
                    number = grid[y][x]
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        b = 0 <= nx < len(grid) and 0 <= ny < len(grid[0])
                        if (b and grid[ny][nx] != number) or not b:
                            visited_fences.append((ny, nx))

                hori, _ = find_consecutive_positions(visited_fences)
                flatten_hori = [x for xs in hori for x in xs]
                # total is the amount of side we have we have found in the last find consecutive positins plus the side that where found in visited fences but not part of a side
                # empty_pos = sum([1 for x in visited_fences if x not in flatten_hori])
                total_sides += len(hori)# + empty_pos
                # print(visited_fences, hori, len(hori), empty_pos)
                total_visited_fences.extend(flatten_hori)

            # print(total_visited_fences)
            # print(total_sides)

            for col in vertical:
                visited_fences = []

                for pos in col:
                    y, x = pos
                    number = grid[y][x]
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        b = 0 <= nx < len(grid) and 0 <= ny < len(grid[0])
                        if (b and grid[ny][nx] != number) or not b:
                            visited_fences.append((ny, nx))

                _, verti = find_consecutive_positions(visited_fences)
                flatten_verti = [x for xs in verti for x in xs]
                # total is the amount of side we have we have found in the last find consecutive positins plus the side that where found in visited fences but not part of a side
                # empty_pos = sum([1 for x in visited_fences if x not in flatten_verti])
                total_sides += len(verti)# + empty_pos
                total_visited_fences.extend(flatten_verti)

            # Now do a final big pass on all the positions that do not have a fence yet and aren't part of a side
            for pos in group:
                x, y = pos
                number = grid[y][x]
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if (nx, ny) in total_visited_fences:
                        total_visited_fences.remove((nx, ny))
                    else:
                        if (nx, ny) not in group:
                            total_sides += 1


        perimeter += len(group) * p
        p2 += len(group) * total_sides

    print("part1,", perimeter)
    print("part2,", p2)



@profiler
def part_two(grid):
    """Comment"""


if __name__ == "__main__":
    # Get input data
    input_data = get_input("inputs/12_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
