# pylint: disable=line-too-long
"""
Part 1: What is the total distance between the two input lists, when they've been sorted?
Answer: 2031679

Part 2: What is the similarity score between the two lists?
Answer: 19678534
"""

from utils import profiler


def get_input(file_path: str) -> tuple[list, list]:
    """Get the input data"""
    lst1, lst2 = [], []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip().split(" ")
            lst1.append(int(line[0]))
            lst2.append(int(line[-1]))

    return lst1, lst2


@profiler
def part_1(lst1: list, lst2: list) -> int:
    """Calculate the pairwise difference between the two lists"""
    return sum([abs(l - r) for l, r in zip(sorted(lst1), sorted(lst2))])


@profiler
def part_2(lst1: list, lst2: list) -> int:
    """Calculate the similarity score, if it occurs in the right list then count it's appearances times the actual number"""
    return sum([i * lst2.count(i) for i in lst1])


if __name__ == "__main__":
    left_lst, right_lst = get_input("inputs/1_input.txt")

    print(f"Part 1: {part_1(left_lst, right_lst)}")
    print(f"Part 2: {part_2(left_lst, right_lst)}")
