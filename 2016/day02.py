# pylint: disable=line-too-long
"""
Part 1: Traverse a keypad to punch a specific code
Answer: 56855

Part 2: The keypad is different but still same thing
Answer: B3C27
"""

from utils import profiler


def get_input(file_path: str) -> list:
    """Get the input data"""
    instructions = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            instructions.append(list(line.strip()))

    return instructions


def dict_value(my_dict: dict, pos: tuple[int, int]) -> str:
    """Bit dumb, find our keygrid position in the values and get back the key"""
    return list(my_dict.keys())[list(my_dict.values()).index(pos)]


def move(instruction: str, moves: list, pos: tuple[int, int]) -> tuple[int, int]:
    """Make a move in the grid based on current options"""
    if instruction not in moves:
        return pos
    elif instruction == "U":
        pos[1] -= 1
    elif instruction == "L":
        pos[0] -= 1
    elif instruction == "R":
        pos[0] += 1
    elif instruction == "D":
        pos[1] += 1

    return pos


@profiler
def execute_instructions(instructions: list, keypad: dict, movement: dict) -> str:
    """Execute a set of instructions based on certain movement options we can do"""
    keylock = []
    pos = [2, 2]

    for instruction in instructions:
        for i in instruction:
            # Get the current position on the grid
            number = dict_value(keypad, pos)
            pos = move(i, movement[number], pos)

        keylock.append(dict_value(keypad, pos))

    # Make a list of strings to a single number
    return ''.join(map(str, keylock))


if __name__ == "__main__":
    instr = get_input("inputs/2_input.txt")

    # Translate positions on the grid back to a number for the keypad
    keypad_part_1 = {"1":[1,1], "2":[2,1], "3":[3,1], "4":[1,2], "5":[2,2], "6":[3,2], "7":[1,3], "8":[2,3], "9":[3,3]}
    keypad_part_2 = {"1":[3,1], "2":[2,2], "3":[3,2], "4":[4,2], "5":[1,3], "6":[2,3], "7":[3,3], "8":[4,3], "9":[5,3],
                     "A":[2,4], "B":[3,4], "C":[4,4], "D":[3,5]}

    # Possible movement options for each position on the grid
    movement_part_1 = {"1":["D", "R"], "2":["L", "R", "D"], "3":["L", "D"], "4":["U", "R", "D"], "5":["U", "D", "L", "R"],
                       "6":["U", "L", "D"], "7":["U", "R"], "8":["U", "L", "R"], "9":["U", "L"]}
    movement_part_2 = {"1":["D"], "2":["R", "D"], "3":["U", "D", "L", "R"], "4":["L", "D"], "5":["R"],
                       "6":["U", "D", "L", "R"], "7":["U", "D", "L", "R"], "8":["U", "D", "L", "R"], "9":["L"], 
                       "A":["U", "R"], "B":["U", "D", "L", "R"], "C":["L", "U"], "D":["U"]}

    print(f"Part 1: {execute_instructions(instr, keypad_part_1, movement_part_1)}")
    print(f"Part 2: {execute_instructions(instr, keypad_part_2, movement_part_2)}")
