# pylint: disable=line-too-long
"""
Part 1: Find all of the directories with a total size of at most 100000. What is the sum of the total sizes of those directories?
Answer: 1583951

Part 2: Find the smallest directory that, if deleted, would free up enough space on the filesystem to run the update. What is the total size of that directory?
Answer: 214171
"""

from utils import profiler


def get_input(file_path: str) -> dict:
    """
    We parse the input to build a filesystem dictionary where each key is a directory path (as a tuple of directory names), 
    and the value is a list of files and subdirectories under that directory.
    Files are represented with their sizes, and directories are marked with a size of 0.
    """
    filesystem = {}
    current_path = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line.startswith("$ cd"):
                # Changing directory
                path = line.split(" ")[2]
                if path == "..":
                    current_path.pop()
                else:
                    current_path.append(path)
            elif line.startswith("$ ls"):
                continue
            else:
                # File or directory listing
                size, name = line.split(" ", 1)
                # If it's a file, we capture its size, dirs have 0 size
                size = int(size) if size != "dir" else 0

                # Traverse the path to ensure all directories are created
                full_path = tuple(current_path)
                if full_path not in filesystem:
                    filesystem[full_path] = []

                filesystem[full_path].append((name, size))

    return filesystem


def calculate_sizes(filesystem):
    """"
    We recursively calculate the total size of each directory. If the directory contains subdirectories, 
    their sizes are calculated and included in the total size.
    """
    directory_sizes = {}

    def get_size(path):
        if path in directory_sizes:
            return directory_sizes[path]

        total_size = 0
        for name, size in filesystem.get(path, []):
            # It's a file else it's a directory and we will recursiively get its size
            if size > 0:
                total_size += size
            else:
                total_size += get_size(path + (name,))

        directory_sizes[path] = total_size
        return total_size

    # Calculate sizes for all directories
    for path in filesystem:
        get_size(path)

    return directory_sizes


@profiler
def part_1(filesystem):
    """"We sum the sizes of all directories that are smaller than 100000"""
    directory_sizes = calculate_sizes(filesystem)

    # Part 1: Find the sum of the sizes of all directories smaller than 100000
    return sum(size for size in directory_sizes.values() if size <= 100000)


@profiler
def part_2(filesystem, total_disk_space=70000000, required_free_space=30000000):
    """
    We calculate the total used space and determine how much free space is needed to meet the required free space. 
    The solution to Part 2 is the size of the smallest directory that can be deleted to free up enough space.
    """
    directory_sizes = calculate_sizes(filesystem)

    # Get the root directory
    used_space = directory_sizes['/',]
    free_space = total_disk_space - used_space
    space_needed = required_free_space - free_space

    return min((size for size in directory_sizes.values() if size >= space_needed), default=None)


if __name__ == "__main__":
    input_data = get_input("inputs/7_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
