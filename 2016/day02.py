# pylint: disable=line-too-long
"""
Day 2: Bathroom Security

Part 1: Traverse a keypad to punch a specific code  
Answer: 56855

Part 2: The keypad is different but still same thing as part 1
Answer: B3C27
"""

from typing import List, Dict,Tuple
from utils import profiler


def get_input(file_path: str) -> List[List[str]]:
    """
    Parses the input file into a List of instruction lines.

    Args:
        file_path (str): Path to the input file.

    Returns:
        List[List[str]]: A list of lists of directional instructions.
    """
    instructions = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            instructions.append(list(line.strip()))
    return instructions


def get_key_by_position(keypad: Dict[str, Tuple[int, int]], position: Tuple[int, int]) -> str:
    """
    Returns the keypad key corresponding to a given position.

    Args:
        keypad (Dict): Mapping of keys to (x, y) positions.
        position (Tuple[int, int]): Current position on the keypad.

    Returns:
        str: The key at the specified position.
    """
    for key, pos in keypad.items():
        if pos == position:
            return key
    raise ValueError(f"Position {position} not found on keypad.")


def move(direction: str, allowed_moves: list[str], position: Tuple[int, int]) -> Tuple[int, int]:
    """
    Moves the current position based on the direction, if allowed.

    Args:
        direction (str): Direction to move ('U', 'D', 'L', 'R').
        allowed_moves (list[str]): Valid directions from current key.
        position (Tuple[int, int]): Current (x, y) position.

    Returns:
        Tuple[int, int]: New (x, y) position after movement.
    """
    x, y = position
    if direction not in allowed_moves:
        return position
    if direction == "U":
        y -= 1
    elif direction == "D":
        y += 1
    elif direction == "L":
        x -= 1
    elif direction == "R":
        x += 1
    return (x, y)


@profiler
def execute_instructions(instructions: List[List[str]], keypad: Dict[str, Tuple[int, int]], movement: Dict[str, List[str]]) -> str:
    """
    Executes a sequence of movement instructions on a keypad.

    Args:
        instructions (List[List[str]]): List of instruction sequences.
        keypad (dict): Keypad layout mapping keys to positions.
        movement (dict): Allowed moves from each key.

    Returns:
        str: Final bathroom code.
    """
    code = []
    position = (2, 2)  # Starting at '5' for both keypads

    for sequence in instructions:
        for direction in sequence:
            current_key = get_key_by_position(keypad, position)
            position = move(direction, movement[current_key], position)
        code.append(get_key_by_position(keypad, position))

    return ''.join(code)


if __name__ == "__main__":
    input_data = get_input("inputs/2_input.txt")

    keypad_part_1 = {
        "1": (1, 1), "2": (2, 1), "3": (3, 1),
        "4": (1, 2), "5": (2, 2), "6": (3, 2),
        "7": (1, 3), "8": (2, 3), "9": (3, 3),
    }

    keypad_part_2 = {
        "1": (3, 1), "2": (2, 2), "3": (3, 2), "4": (4, 2),
        "5": (1, 3), "6": (2, 3), "7": (3, 3), "8": (4, 3), "9": (5, 3),
        "A": (2, 4), "B": (3, 4), "C": (4, 4), "D": (3, 5),
    }

    movement_part_1 = {
        "1": ["D", "R"], "2": ["L", "D", "R"], "3": ["L", "D"],
        "4": ["U", "D", "R"], "5": ["U", "D", "L", "R"], "6": ["U", "D", "L"],
        "7": ["U", "R"], "8": ["U", "L", "R"], "9": ["U", "L"]
    }

    movement_part_2 = {
        "1": ["D"], "2": ["D", "R"], "3": ["L", "R", "U", "D"], "4": ["L", "D"],
        "5": ["R"], "6": ["U", "D", "L", "R"], "7": ["U", "D", "L", "R"],
        "8": ["U", "D", "L", "R"], "9": ["L"], "A": ["U", "R"],
        "B": ["U", "D", "L", "R"], "C": ["U", "L"], "D": ["U"]
    }

    print(f"Part 1: {execute_instructions(input_data, keypad_part_1, movement_part_1)}")
    print(f"Part 2: {execute_instructions(input_data, keypad_part_2, movement_part_2)}")
