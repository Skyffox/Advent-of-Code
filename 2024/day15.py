# pylint: disable=line-too-long
"""
Day 15: Warehouse Woes

Part 1: Predict the motion of the robot and boxes in the warehouse. After the robot is finished moving, what is the sum of all boxes GPS coordinates?
Answer: 1479679

Part 2: Predict the motion of the robot and boxes in this new, scaled-up warehouse. What is the sum of all boxes final GPS coordinates?
Answer: 1509780
"""

from typing import List, Tuple, Set
from utils import profiler


def get_input(file_path: str) -> Tuple[List[List[str]], List[str]]:
    """
    Read the input file and return grid and movement instructions.

    Returns:
        tuple[list[list[str]], list[str]]: The grid layout and robot movement instructions.
    """
    grid, instructions = [], []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = list(line.strip())
            if line and line[0] == "#":
                grid.append(line)
            elif line != []:
                instructions.extend(line)

    return grid, instructions


def separate_input(grid: List[List[str]]) -> Tuple[Tuple[int, int], List[Tuple[int, int]], Set[Tuple[int, int]]]:
    """
    Parse the grid into robot start position, box locations, and wall positions.

    Returns:
        tuple: Start position, list of box positions, and set of wall coordinates.
    """
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
                boxes.append(((x, y), (x + 1, y)))

    return start, boxes, walls


@profiler
def part_one(grid: List[List[str]], instructions: List[str]) -> int:
    """
    Simulate the robot's movement in the warehouse according to the instructions.
    The robot can push boxes into empty spaces but cannot push into walls or stacked boxes.

    Returns:
        int: Sum of all box GPS coordinates (100*y + x).
    """
    robot_pos, boxes, walls = separate_input(grid)
    directions = {"<": (-1, 0), ">": (1, 0), "^": (0, -1), "v": (0, 1)}

    for instruction in instructions:
        dx, dy = directions[instruction]
        next_x, next_y = robot_pos[0] + dx, robot_pos[1] + dy
        next_pos = (next_x, next_y)

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
                box_x += dx
                box_y += dy
        else:
            robot_pos = next_pos

    # Find the sum of all boxes GPS coordinates after the robot finishes moving
    return sum([100 * y + x for x, y in boxes])


def move_boxes(dx: int, dy: int, box_index: int, boxes: List[Tuple[Tuple[int, int], Tuple[int, int]]], walls: Set[Tuple[int, int]], box_set: Set[Tuple[int, int]]) -> Tuple[bool, Set[int]]:
    """
    Recursive function to attempt pushing multiple connected boxes in the given direction.

    Returns:
        tuple[bool, set]: Whether move was possible, and which box indices were moved.
    """
    # Indices of boxes that need to be moved
    boxes_to_be_moved = [box_index]
    left_box, right_box = boxes[box_index]

    # Determine the new position for the current box
    new_left = (left_box[0] + dx, left_box[1] + dy)
    new_right = (right_box[0] + dx, right_box[1] + dy)

    # We do not execute a move if we were to move into a wall
    if new_left in walls or new_right in walls:
        return False, set()
    # If it is not in the box_set it means it is an empty space and we can move this particular box
    if new_left not in box_set and new_right not in box_set:
        return True, set(boxes_to_be_moved)

    # If the new location of a box turns out to contain a box, then we need to do the same for those boxes
    box_indices = [idx for idx, box in enumerate(boxes) if (new_left in box or new_right in box) and idx != box_index]

    for idx in box_indices:
        can_move, new_boxes = move_boxes(dx, dy, idx, boxes, walls, box_set)
        if not can_move:
            return False, set()
        boxes_to_be_moved += new_boxes

    return True, set(boxes_to_be_moved)


@profiler
def part_two(grid: List[List[str]], instructions: List[str]) -> int:
    """
    Simulate the robot's movement in the scaled-up warehouse with double-width boxes.
    Here, boxes occupy two horizontal positions, and can push each other as a chain.

    ##############          ##############
    ##..........##          ##..........##
    ##..........##          ##...[][]...##
    ##...[][]...##   -->    ##....[]....##
    ##....[]....##          ##.....@....##
    ##.....@....##          ##..........##
    ##############          ##############

    Returns:
        int: Sum of all final box GPS coordinates (100*y + x of the left side of each box).
    """
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
    directions = {"<": (-1, 0), ">": (1, 0), "^": (0, -1), "v": (0, 1)}
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

    return sum([100 * y + x for (x, y), _ in boxes])


if __name__ == "__main__":
    input_grid, input_instructions = get_input("inputs/15_input.txt")

    print(f"Part 1: {part_one(input_grid, input_instructions)}")
    print(f"Part 2: {part_two(input_grid, input_instructions)}")
