# pylint: disable=line-too-long
"""
Part 1: Calculate the eventual frequency we end up on
Answer: 505

Part 2: Find the frequency we land on twice for the first time
Answer: 72330 (take ~80 seconds)
"""

from utils import profiler


def get_input(file_path: str) -> tuple[list, list]:
    """Get the input data"""
    lst = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            # print(line)
            lst.append(int(line.strip()))

    return lst


@profiler
def part_1(lst: list) -> int:
    """The input is just some additions or subtractions, so in Python we can just take the sum() of those"""
    return sum(lst)


@profiler
def part_2(lst: list) -> int:
    """Return the frequency we have already seen"""
    seen_frequencies = [0]
    while True:
        for f in lst:
            curr_freq = seen_frequencies[-1] + f
            if curr_freq in seen_frequencies:
                return curr_freq

            seen_frequencies.append(curr_freq)


if __name__ == "__main__":
    input_data = get_input("inputs/1_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
