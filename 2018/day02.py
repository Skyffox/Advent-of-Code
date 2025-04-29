# pylint: disable=line-too-long
"""
Part 1: Calculate the checksum of IDs that contain two of any letter or three of any letter
Answer: 7192

Part 2: Find the two IDs that are matching but are off by one
Answer: mbruvapghxlzycbhmfqjonsie
"""

from utils import profiler


def get_input(file_path: str) -> list:
    """Get the input data"""
    with open(file_path, "r", encoding="utf-8") as file:
        return [list(line.strip()) for line in file]


@profiler
def part_1(lst: list) -> int:
    """Count amount of times a line contains a character 2 or 3 times"""
    doubles, triples = 0, 0
    for line in lst:
        occurences = [line.count(x) for x in set(line)]

        if 2 in occurences:
            doubles += 1
        if 3 in occurences:
            triples += 1

    return doubles * triples


@profiler
def part_2(lst: list) -> str:
    """Compare two lists, if the lists are off by one we have a match"""
    for idx, lst1 in enumerate(lst):
        for lst2 in lst[idx:]:
            # Return True or False for each comparison between two lists
            matches = [lst1[idx] == lst2[idx] for idx in range(len(lst1))]
            if matches.count(False) == 1:
                wrong_index = matches.index(False)
                lst1.pop(wrong_index)

                return "".join(lst1)


if __name__ == "__main__":
    input_data = get_input("inputs/2_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
