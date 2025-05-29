# pylint: disable=line-too-long
"""
Day 13: Care Package

Part 1: How many block tiles are on the screen when the game exits?
Answer: 398

Part 2: Beat the game by breaking all the blocks. What is your score after the last block is broken?
Answer: 1664
"""

from typing import Dict, List, Tuple
from utils import IntcodeComputer
from utils import profiler


def get_input(file_path: str) -> List[int]:
    """
    Reads the input file and returns the Intcode program as a list of integers.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        List[int]: The Intcode program.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return list(map(int, file.read().strip().split(",")))


@profiler
def part_one(program: List[int]) -> int:
    """
    Runs the program to build the screen and counts the number of block tiles (tile_id == 2).

    Args:
        program (List[int]): Intcode program.

    Returns:
        int: Number of block tiles on the screen.
    """
    computer = IntcodeComputer(program.copy())
    outputs = []
    while not computer.halted:
        val = computer.run()
        if val is not None:
            outputs.append(val)

    # Outputs come in triples: (x, y, tile_id)
    tiles = [outputs[i + 2] for i in range(0, len(outputs), 3)]
    return tiles.count(2) # Count of block tiles



@profiler
def part_two(program: List[int]) -> int:
    """
    Plays the game by controlling the joystick and returns the final score.

    Args:
        program (List[int]): Intcode program.

    Returns:
        int: Final game score after breaking all blocks.
    """
    memory = program.copy()
    memory[0] = 2 # Play for free by setting memory address 0 to 2
    computer = IntcodeComputer(memory)

    screen: Dict[Tuple[int, int], int] = {}
    score = 0

    ball_x = 0
    paddle_x = 0

    output_buffer = []

    while not computer.halted:
        val = computer.run()
        if val is not None:
            output_buffer.append(val)
            if len(output_buffer) == 3:
                x, y, tile_id = output_buffer
                output_buffer.clear()
                if (x, y) == (-1, 0):
                    score = tile_id  # Update score
                else:
                    screen[(x, y)] = tile_id
                    if tile_id == 3:
                        paddle_x = x
                    elif tile_id == 4:
                        ball_x = x
        else:
            # Computer is waiting for input
            # Decide joystick input based on ball and paddle positions
            if ball_x > paddle_x:
                joystick = 1
            elif ball_x < paddle_x:
                joystick = -1
            else:
                joystick = 0
            computer.add_input(joystick)

    return score



if __name__ == "__main__":
    input_data = get_input("inputs/13_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
