# pylint: disable=line-too-long
"""
Day 7: No Space Left On Device

Part 1: Find all of the directories with a total size of at most 100000. What is the sum of the total sizes of those directories?
Answer: 1583951

Part 2: Find the smallest directory that, if deleted, would free up enough space on the filesystem to run the update. What is the total size of that directory?
Answer: 214171
"""

from typing import Dict, Tuple, List
from utils import profiler


def get_input(file_path: str) -> Dict[Tuple[str, ...], List[Tuple[str, int]]]:
    """
    Parses the input file into a simulated filesystem.

    Each directory is represented by a path tuple, and contains a list of its contents.
    Files have an associated size; directories are listed with size 0.

    Args:
        file_path (str): Path to the input file.

    Returns:
        dict: A mapping of directory paths to their contents.
    """
    filesystem = {}
    current_path = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line.startswith("$ cd"):
                # Navigate directories
                target = line.split(" ")[2]
                if target == "..":
                    current_path.pop()
                elif target == "/":
                    current_path = ["/"]
                else:
                    current_path.append(target)
            elif line.startswith("$ ls"):
                continue
            else:
                size_str, name = line.split(" ", 1)
                # If it's a file, we capture its size, dirs have 0 size
                size = int(size_str) if size_str != "dir" else 0
                full_path = tuple(current_path)

                if full_path not in filesystem:
                    filesystem[full_path] = []

                filesystem[full_path].append((name, size))

    return filesystem


def calculate_sizes(filesystem: Dict[Tuple[str, ...], List[Tuple[str, int]]]) -> Dict[Tuple[str, ...], int]:
    """
    Recursively calculates the total size of each directory.

    Args:
        filesystem (dict): The simulated filesystem structure.

    Returns:
        dict: A mapping of directory paths to their total sizes.
    """
    directory_sizes = {}

    def get_size(path: Tuple[str, ...]) -> int:
        if path in directory_sizes:
            return directory_sizes[path]

        total_size = 0
        for name, size in filesystem.get(path, []):
            if size > 0:
                total_size += size
            else:
                total_size += get_size(path + (name,))

        directory_sizes[path] = total_size
        return total_size

    for path in filesystem:
        get_size(path)

    return directory_sizes


@profiler
def part_1(filesystem: Dict[Tuple[str, ...], List[Tuple[str, int]]]) -> int:
    """
    Sums the sizes of all directories whose total size does not exceed 100000.

    Args:
        filesystem (dict): The parsed filesystem.

    Returns:
        int: The total size of all qualifying directories.
    """
    sizes = calculate_sizes(filesystem)
    return sum(size for size in sizes.values() if size <= 100_000)


@profiler
def part_2(
    filesystem: Dict[Tuple[str, ...], List[Tuple[str, int]]],
    total_disk_space: int = 70_000_000,
    required_free_space: int = 30_000_000
) -> int:
    """
    Finds the smallest directory that can be deleted to free up enough space.

    Args:
        filesystem (dict): The parsed filesystem.
        total_disk_space (int): Total available disk space.
        required_free_space (int): Space needed after cleanup.

    Returns:
        int: Size of the smallest deletable directory that satisfies the constraint.
    """
    sizes = calculate_sizes(filesystem)
    used_space = sizes[('/',)]
    current_free = total_disk_space - used_space
    needed_space = required_free_space - current_free

    return min((size for size in sizes.values() if size >= needed_space), default=0)


if __name__ == "__main__":
    input_data = get_input("inputs/7_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
