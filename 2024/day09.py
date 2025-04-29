# pylint: disable=line-too-long
"""
Part 1: Find free disk space and switch file memory to the empty space, NOTE: do not use list.index() ever again
Answer: 6435922584968

Part 2: Instead of being memory inefficient switch the entire file to the free disk space (disk space must be continuous)
Answer: 6469636832766
"""

from utils import profiler


def checksum(disk_space: list) -> int:
    """Calculate the checksum, based on the index and fileID number"""
    return sum([idx * num for idx, num in enumerate(disk_space) if num != "."])


def get_input(file_path: str) -> tuple[list, list, dict, list]:
    """Get the input data"""
    disk_space, empty_space = [], []
    disk_space_range, empty_space_range = {}, []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            actual_pos = 0
            for idx, num in enumerate(line):
                num = int(num)
                if idx % 2 == 0:
                    disk_space.extend([idx // 2] * num)
                    # We want to know the bounds where the number is, because list.index() is terribly slow
                    disk_space_range[idx // 2] = [actual_pos, actual_pos + num - 1]
                    actual_pos += num
                else:
                    disk_space.extend(["."] * num)
                    empty_space.extend(list(range(actual_pos, actual_pos + num)))
                    # For part 2 it is much easier to iterate over a range of empty positions
                    empty_space_range.append(list(range(actual_pos, actual_pos + num)))
                    actual_pos += num

    return disk_space, empty_space, disk_space_range, empty_space_range


@profiler
def part_1(disk_space: list, empty_space: list) -> int:
    """Switch the positions of memory cells with an empty space as far left to it as possible"""
    for num_index in range(len(disk_space) - 1, 0, -1):
        if disk_space[num_index] != ".":
            # Get the index of the first possible space
            dot_index = empty_space.pop(0)

            # We only want to move the data to the left, so once our empty spot is to the right we can stop
            if dot_index > num_index:
                break

            # Swap the part of the file with an empty space
            disk_space[dot_index] = disk_space[num_index]
            disk_space[num_index] = "."

    return checksum(disk_space)


@profiler
def part_2(disk_space: list, disk_space_range: dict, empty_space_range: list) -> int:
    """Instead of moving one memory cell we move the entire block of same memory as far left as possible"""
    num_index = len(disk_space) - 1
    numbers_moved = []
    while num_index > 1:
        number = disk_space[num_index]
        # Since we are iterating over the entire list, we need to know when we are
        # encountering numbers we have already moved, since we don't need to move them again
        if number != "." and number not in numbers_moved:
            # Get the start and end position where the number occurs in our input
            start_idx, end_idx = disk_space_range[number][0], disk_space_range[number][-1]
            l = end_idx - start_idx + 1

            for empty_idx, empty_space in enumerate(empty_space_range):
                # We only want to move the data to the left, so once our empty spot is to the right of our current position we can stop
                if empty_space != [] and empty_space[0] > num_index:
                    break
                if len(empty_space) >= l:
                    # If we find a suitable empty spot we swap the empty and number entries
                    disk_space[empty_space[0]:empty_space[l-1]+1] = [number] * l
                    disk_space[start_idx:end_idx+1] = ["."] * l

                    # Remove the empty spots from our list
                    empty_space_range[empty_idx] = empty_space[l:]
                    break

            num_index -= l
            numbers_moved.append(number)
        else:
            num_index -= 1

    return checksum(disk_space)


if __name__ == "__main__":
    # Get input data
    memory, empty, memory_range, empty_range = get_input("inputs/9_input.txt")

    # Use same input for Part 2
    memory_cpy = memory[::]

    print(f"Part 1: {part_1(memory, empty)}")
    print(f"Part 2: {part_2(memory_cpy, memory_range, empty_range)}")
