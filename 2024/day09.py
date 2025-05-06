# pylint: disable=line-too-long
"""
Day 9: Disk Fragmenter

Part 1: Find free disk space and switch file memory to the empty space, NOTE: do not use list.index() ever again
Answer: 6435922584968

Part 2: Instead of being memory inefficient, switch the entire file to the free disk space (disk space must be continuous)
Answer: 6469636832766
"""

from typing import List, Dict, Tuple
from utils import profiler


def checksum(disk_space: List[str]) -> int:
    """
    Calculate the checksum of the disk space.

    The checksum is calculated by summing the products of the index and value of each non-empty memory cell
    (denoted by any number other than the placeholder "."). This gives a value based on the positions and types
    of data stored in the disk space.

    Args:
        disk_space (List[str]): A list representing the disk space, where each element is either a number or a placeholder.

    Returns:
        int: The checksum of the disk space, which is the sum of the index-value products for non-empty cells.
    """
    return sum([idx * num for idx, num in enumerate(disk_space) if num != "."])


def get_input(file_path: str) -> Tuple[List[str], List[int], Dict[int, List[int]], List[List[int]]]:
    """
    Reads the disk space configuration from the input file and parses it into structures.

    Args:
        file_path (str): The path to the input file containing the disk space configuration.

    Returns:
        Tuple: A tuple containing:
            - disk_space (List[str]): A list representing the disk space, with numbers indicating memory and "." indicating empty space.
            - empty_space (List[int]): A list of indices where empty space occurs, denoted by ".".
            - disk_space_range (Dict[int, List[int]]): A dictionary mapping each memory number to its occupied index range.
            - empty_space_range (List[List[int]]): A list of ranges representing where empty space occurs.
    """
    disk_space, empty_space = [], []
    disk_space_range, empty_space_range = {}, []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            actual_pos = 0
            for idx, num in enumerate(line):
                num = int(num)
                if idx % 2 == 0:
                    disk_space.extend([idx // 2] * num)
                    # Track the range of the current number in disk space
                    disk_space_range[idx // 2] = [actual_pos, actual_pos + num - 1]
                    actual_pos += num
                else:
                    disk_space.extend(["."] * num)
                    empty_space.extend(list(range(actual_pos, actual_pos + num)))
                    # Keep track of empty space ranges for part 2
                    empty_space_range.append(list(range(actual_pos, actual_pos + num)))
                    actual_pos += num

    return disk_space, empty_space, disk_space_range, empty_space_range


@profiler
def part_1(disk_space: List[str], empty_space: List[int]) -> int:
    """
    This function simulates the movement of memory cells into empty spaces. It finds the rightmost non-empty memory cell
    and moves it as far left as possible, using available empty spaces. The function then calculates and returns the checksum.

    Args:
        disk_space (List[str]): A list representing the disk space.
        empty_space (List[int]): A list of indices where empty space is located.

    Returns:
        int: The checksum of the disk space after moving the memory cells.
    """
    for num_index in range(len(disk_space) - 1, 0, -1):
        if disk_space[num_index] != ".":
            # Get the index of the first possible empty space
            dot_index = empty_space.pop(0)

            # Stop if the empty space is to the right of the current memory cell
            if dot_index > num_index:
                break

            # Move the memory cell to the empty space
            disk_space[dot_index] = disk_space[num_index]
            disk_space[num_index] = "."

    return checksum(disk_space)


@profiler
def part_2(disk_space: List[str], disk_space_range: Dict[int, List[int]], empty_space_range: List[List[int]]) -> int:
    """
    In this part, instead of moving one memory cell at a time, the function moves entire blocks of memory (numbers)
    to the left as far as possible, utilizing available empty spaces. Once the memory blocks are moved, the function
    calculates and returns the checksum of the disk space.

    Args:
        disk_space (List[str]): A list representing the disk space.
        disk_space_range (Dict[int, List[int]]): A dictionary mapping memory numbers to their position ranges in the disk space.
        empty_space_range (List[List[int]]): A list of ranges representing available empty space on the disk.

    Returns:
        int: The checksum of the disk space after moving the memory blocks.
    """
    num_index = len(disk_space) - 1
    numbers_moved = []

    while num_index > 1:
        number = disk_space[num_index]
        # Skip already moved numbers
        if number != "." and number not in numbers_moved:
            # Get the range of positions occupied by this memory block
            start_idx, end_idx = disk_space_range[number][0], disk_space_range[number][-1]
            l = end_idx - start_idx + 1

            for empty_idx, empty_space in enumerate(empty_space_range):
                # Stop if the empty space is beyond the current memory block's position
                if empty_space != [] and empty_space[0] > num_index:
                    break

                if len(empty_space) >= l:
                    # If enough space is found, move the memory block
                    disk_space[empty_space[0]:empty_space[l-1]+1] = [number] * l
                    disk_space[start_idx:end_idx+1] = ["."] * l

                    # Remove the empty spots that were used
                    empty_space_range[empty_idx] = empty_space[l:]
                    break

            num_index -= l
            numbers_moved.append(number)
        else:
            num_index -= 1

    return checksum(disk_space)


if __name__ == "__main__":
    memory, empty, memory_range, empty_range = get_input("inputs/9_input.txt")

    # Use same input for Part 2
    memory_cpy = memory[::]

    print(f"Part 1: {part_1(memory, empty)}")
    print(f"Part 2: {part_2(memory_cpy, memory_range, empty_range)}")
