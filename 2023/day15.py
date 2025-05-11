# pylint: disable=line-too-long
"""
Day 15: Lens Library

Part 1: Apply the custom hash algorithm to each step and sum the results.
Answer: 510273

Part 2: Simulate lens operations in a series of boxes and compute total focusing power.
Answer: 212449
"""

from typing import List, Dict, Tuple
from utils import profiler


def get_input(file_path: str) -> List[str]:
    """
    Parses the initialization sequence from the input file.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        List[str]: List of instruction strings separated by commas.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read().strip().split(",")


def hash_label(label: str) -> int:
    """
    Computes the HASH value for a given label using a custom algorithm.

    Args:
        label (str): The string to hash.

    Returns:
        int: The resulting hash value (0–255).
    """
    value = 0
    for char in label:
        value = (value + ord(char)) * 17 % 256
    return value


@profiler
def part_one(instructions: List[str]) -> int:
    """
    Solves Part 1 by applying the custom HASH algorithm to each step.

    Args:
        instructions (List[str]): List of initialization step strings.

    Returns:
        int: Sum of all resulting hash values.
    """
    return sum(hash_label(instr) for instr in instructions)


@profiler
def part_two(instructions: List[str]) -> int:
    """
    Simulates a series of lens operations into 256 labeled boxes, then computes the total focusing power.

    Rules:
    - Each instruction is either:
        a) `{label}-{}`: remove any lens with this label from its hashed box.
        b) `{label}={focal_length}`: insert/update a lens with the given focal length.
    - Each box contains a list of lenses ordered by insertion.
    - Focusing power = (box_num + 1) × (slot_index + 1) × focal_length

    Args:
        instructions (List[str]): The list of operations to perform.

    Returns:
        int: Total focusing power after all instructions.
    """
    boxes: Dict[int, List[Tuple[str, int]]] = {i: [] for i in range(256)}

    for instr in instructions:
        if '=' in instr:
            label, value = instr.split('=')
            focal_len = int(value)
            box_num = hash_label(label)

            # Update if label exists, else append
            for i, (existing_label, _) in enumerate(boxes[box_num]):
                if existing_label == label:
                    boxes[box_num][i] = (label, focal_len)
                    break
            else:
                boxes[box_num].append((label, focal_len))

        elif '-' in instr:
            label = instr[:-1]
            box_num = hash_label(label)
            boxes[box_num] = [item for item in boxes[box_num] if item[0] != label]

    # Calculate focusing power
    total_power = 0
    for box_num, lenses in boxes.items():
        for slot_index, (_, focal_len) in enumerate(lenses):
            total_power += (box_num + 1) * (slot_index + 1) * focal_len

    return total_power


if __name__ == "__main__":
    input_data = get_input("inputs/15_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
