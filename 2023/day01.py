# pylint: disable=line-too-long
"""
Part 1: Get the numeric calibration values from the input
Answer: 54081

Part 2: Get the calibration values like in part 1 whilst converting digits in their alfabetic form to their numeric form
Answer: 54649
"""

from utils import profiler


def get_input(file_path: str) -> list:
    """Get the input data"""
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file]


@profiler
def part_1(lines: list) -> int:
    """Get all numeric values from the input"""
    n = 0
    for line in lines:
        numbers = [str(x) for x in line if x.isnumeric()]
        if numbers != []:
            n += int("".join([numbers[0], numbers[-1]]))

    return n


@profiler
def part_2(lines: list) -> int:
    """Do the same as part 1 but convert non numeric values to their alfanumeric value"""
    digits = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    n = 0

    for line in lines:
        while True:
            # Find all indices where we find a number not in numeric notation.
            indices = [(line.find(number), index + 1) for index, number in enumerate(digits) if line.find(number) != -1]
            if indices != []:
                line = list(line)
                # Replace the first index of the number with the numeric equivalent. Cast to list and back so we can mutate.
                for index in indices:
                    line[index[0]] = str(index[1])
                line = "".join(line)
            else:
                break

        # Add the first and last numeric value of the input string.
        numbers = [str(x) for x in line if x.isnumeric()]
        if numbers != []:
            n += int("".join([numbers[0], numbers[-1]]))

    return n


if __name__ == "__main__":
    input_data = get_input("inputs/1_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
