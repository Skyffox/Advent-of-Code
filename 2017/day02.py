# pylint: disable=line-too-long
"""
Part 1: Find the differences between the biggest and smallest number of each row
Answer: 47136

Part 2: See what numbers create an integer when dividing in that same row
Answer: 250
"""

from utils import profiler


def get_input(file_path: str) -> list:
    """Get the input data"""
    inp = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            inp.append(list(map(int, line.strip().split("\t"))))

    return inp


@profiler
def part_1(lst: list) -> int:
    """Find the difference between the biggest and smallest number in a list"""
    return sum([max(x) - min(x) for x in lst])


@profiler
def part_2(lst: list) -> int:
    """Sort first so the big number is divided by the small number"""
    n = 0
    for sublst in lst:
        sublst.sort(reverse=True)
        for idx, i in enumerate(sublst):
            for j in sublst[idx+1:]:
                if (i / j).is_integer():
                    n += i / j

    return int(n)


if __name__ == "__main__":
    input_data = get_input("inputs/2_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
