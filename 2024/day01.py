# pylint: disable=line-too-long
"""
Part 1: Two lists contain location IDs. What is the total distance between your lists?
Answer: 2031679

Part 2: What is the similarity score between the two lists?
Answer: 19678534
"""

from utils import profiler


def get_input(file_path: str) -> tuple[list, list]:
    """Get the input data"""
    left_lst, right_lst = [], []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip().split(" ")
            left_lst.append(int(line[0]))
            right_lst.append(int(line[-1]))

    return left_lst, right_lst


@profiler
def part_1(left_lst: list, right_lst: list) -> int:
    """Calculate the pairwise difference between the two lists"""
    return sum([abs(l - r) for l, r in zip(sorted(left_lst), sorted(right_lst))])


@profiler
def part_2(left_lst: list, right_lst: list) -> int:
    """Calculate the similarity score"""
    return sum([i * right_lst.count(i) for i in left_lst])


if __name__ == "__main__":
    left_input, right_input = get_input("inputs/1_input.txt")

    print(f"Part 1: {part_1(left_input, right_input)}")
    print(f"Part 2: {part_2(left_input, right_input)}")
