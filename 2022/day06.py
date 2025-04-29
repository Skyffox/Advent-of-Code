# pylint: disable=line-too-long
"""
Part 1: How many characters need to be processed before the first start-of-packet marker is detected?
Answer: 1850

Part 2: How many characters need to be processed before the first start-of-message marker is detected?
Answer: 2823
"""

from utils import profiler


def get_input(file_path: str) -> list:
    """Get the input data"""
    with open(file_path, "r", encoding="utf-8") as file:
        return list(file.readline())


@profiler
def compute(lst, num):
    """a"""
    for x in range(len(lst) - num - 1):
        chars = lst[x:x + num]
        if len(chars) == len(set(chars)):
            return x + num


if __name__ == "__main__":
    input_data = get_input("inputs/6_input.txt")

    print(f"Part 1: {compute(input_data, 4)}")
    print(f"Part 2: {compute(input_data, 14)}")
