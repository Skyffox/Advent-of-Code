# pylint: disable=line-too-long
"""
Part 1: Predict the motion of the robot and boxes in the warehouse. After the robot is finished moving, what is the sum of all boxes GPS coordinates?
Answer: 1479679

Part 2: Predict the motion of the robot and boxes in this new, scaled-up warehouse. What is the sum of all boxes final GPS coordinates?
Answer: 1509780
"""

from utils import profiler


def get_input(file_path: str) -> list:
    """Get the input data"""
    grid, instructions = [], []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = list(line.strip())
            if line and line[0] == "#":
                grid.append(line)
            elif line != []:
                instructions.extend(line)

    return grid, instructions


def separate_input(grid: list) -> tuple[tuple[int, int], list, set]:
    """Separate the input into different data structures"""
    start = (0, 0)
    walls = set()
    boxes = []
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            if c == "O":
                boxes.append((x, y))
            elif c == "#":
                walls.add((x, y))
            elif c == "@":
                # Start position of the robot
                start = (x, y)
            elif c == "[":
                # For part 2 we have a wall that occupies 2 horizontal spaces
                # These positions are paired in the same list
                boxes.append(((x, y), (x + 1, y)))

    return start, boxes, walls


@profiler
def part_one(grid, instructions):
    """Read the instructions to make the robot move, simulate the correct behaviour when we encounter a wall or box"""
    robot_pos, boxes, walls = separate_input(grid)
    directions = {"<" : (-1, 0), ">" : (1, 0), "^" : (0, -1), "v" : (0, 1)}

    for instruction in instructions:
        dx, dy = directions[instruction]

        next_x, next_y = robot_pos[0] + dx, robot_pos[1] + dy
        next_pos = (next_x, next_y)

        # We encounter a wall, so don't do anything
        if next_pos in walls:
            continue
        if next_pos in boxes:
            # We encounter a box so we need to check whether we can move it
            box_x, box_y = next_x + dx, next_y + dy
            while (box_x, box_y) not in walls:
                # If we find a space that is not a wall or box it means its empty
                if (box_x, box_y) not in walls and (box_x, box_y) not in boxes:
                    robot_pos = next_pos
                    # Only need to swap the empty space with the box from the next position
                    boxes.remove(next_pos)
                    boxes.append((box_x, box_y))
                    break

                box_x, box_y = box_x + dx, box_y + dy
        else:
            robot_pos = next_pos

    # Find the sum of all boxes GPS coordinates after the robot finishes moving
    return sum([100 * y + x for x, y in boxes])


def move_boxes(dx, dy, box_index, boxes, walls, box_set):
    """Recursive function to keep checking the next space for a box to see if we can move it"""
    # Indices of boxes that need to be moved
    boxes_to_be_moved = [box_index]
    left_box, right_box = boxes[box_index]

    # Determine the new position for the current box
    new_left, new_right = (left_box[0] + dx, left_box[1] + dy), (right_box[0] + dx, right_box[1] + dy)
    # We do not execute a move if we were to move into a wall
    if new_left in walls or new_right in walls:
        return False, None
    # If it is not in the box_set it means it is an empty space and we can move this particular box
    if new_left not in box_set and new_right not in box_set:
        return True, set(boxes_to_be_moved)

    # If the new location of a box turns out to contain a box, then we need to do the same for those boxes
    box_indices = [idx for idx, box in enumerate(boxes) if (new_left in box or new_right in box) and idx != box_index]

    for idx in box_indices:
        can_move, new_boxes = move_boxes(dx, dy, idx, boxes, walls, box_set)
        if not can_move:
            return False, None
        boxes_to_be_moved += new_boxes

    return True, set(boxes_to_be_moved)


@profiler
def part_two(grid, instructions):
    """
    Change the grid based on the new rules, where everything is becoming twice as wide
    We are going to do exactly the same as in part 1 but, because boxes are twice as wide
    we need to account for the fact that the left and right side of the box can move other boxes

    ##############          ##############
    ##..........##          ##..........##
    ##..........##          ##...[][]...##
    ##...[][]...##   -->    ##....[]....##
    ##....[]....##          ##.....@....##
    ##.....@....##          ##..........##
    ##############          ##############
    """
    # Extend everything in the new grid
    new_grid = []
    for line in grid:
        row = []
        for el in line:
            if el == "#":
                row.extend(["#", "#"])
            elif el == "O":
                row.extend(["[", "]"])
            elif el == ".":
                row.extend([".", "."])
            elif el == "@":
                row.extend(["@", "."])

        new_grid.append(row)

    start, boxes, walls = separate_input(new_grid)

    directions = {"<" : (-1, 0), ">" : (1, 0), "^" : (0, -1), "v" : (0, 1)}

    robot_pos = start
    # For this part we want to know which positions are a single box, those positions are saved in the boxes variable
    # This box_set variable is a set of all positions of the boxes
    box_set = set()
    for left_box, right_box in boxes:
        box_set.add(left_box)
        box_set.add(right_box)

    for instruction in instructions:
        dx, dy = directions[instruction]

        next_x, next_y = robot_pos[0] + dx, robot_pos[1] + dy
        next_pos = (next_x, next_y)

        if next_pos in walls:
            continue
        if next_pos in box_set:
            # Find the first matching tuple, the next() function returns the first element from the generator that satisfies the condition
            box_idx = next((idx for idx, box in enumerate(boxes) if next_pos in box), None)

            can_move, boxes_to_be_moved = move_boxes(dx, dy, box_idx, boxes, walls, box_set)
            if can_move:
                robot_pos = next_pos
                for box_idx in boxes_to_be_moved:
                    # Update the position of the walls
                    a, b = boxes[box_idx]
                    ax, ay = a
                    bx, by = b
                    boxes[box_idx] = ((ax + dx, ay + dy), (bx + dx, by + dy))

                # Above the positions of walls can be doubled during the forloop, so we rewrite the set after this forloop
                box_set = set()
                for left_box, right_box in boxes:
                    box_set.add(left_box)
                    box_set.add(right_box)

        else:
            robot_pos = next_pos

    # find the sum of all boxes GPS coordinates after the robot finishes moving
    return sum([100 * y + x for (x, y), _ in boxes])


if __name__ == "__main__":
    # Get input data
    input_grid, input_instructions = get_input("inputs/15_input.txt")

    print(f"Part 1: {part_one(input_grid, input_instructions)}")
    print(f"Part 2: {part_two(input_grid, input_instructions)}")
