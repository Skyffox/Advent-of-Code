# pylint: disable=line-too-long
"""
Part 1: How many stones will you have after blinking 25 times?
Answer: 172484

Part 2: How many stones will you have after blinking 75 times?
Answer: 205913561055242
"""

from utils import profiler


def get_input(file_path: str) -> list:
    """Get the input data"""
    with open(file_path, "r", encoding="utf-8") as file:
        return list(map(int, file.readlines()[0].split(" ")))


def blink(my_dict: dict) -> dict:
    """
    Simulate a single blink for a dictionary of stones. There are 3 rules for a stone during a blink:
    - If the current value is 0 it becomes 1
    - If the length of the current value is divisible by 2, then 2 new stones will have the value of either side of the current value
    - Otherwise the new value is the current value times 2024

    The result is added to a new dictionary because we are interested in the amount of stones, 
    but not in actually computing the result for all of these
    """
    new_dict = {}
    for key, val in my_dict.items():
        if key == 0:
            new_dict[1] = new_dict.get(1, 0) + val
        elif len(str(key)) % 2 == 0:
            left = int(str(key)[len(str(key)) // 2:])
            right = int(str(key)[:len(str(key)) // 2])

            new_dict[left] = new_dict.get(left, 0) + val
            new_dict[right] = new_dict.get(right, 0) + val
        else:
            new_val = key * 2024
            new_dict[new_val] = new_dict.get(new_val, 0) + val

    return new_dict


@profiler
def compute(data_input: list, nr_blinks: int) -> int:
    """
    Perform an amount of blinks for each number in the input
    We can iterate over the input since the result of a blink for a stone is 
    independent of the result of the other stones
    """
    n = 0
    for num in data_input:
        stones = {num : 1}
        for _ in range(nr_blinks):
            stones = blink(stones)

        n += sum(list(stones.values()))

    return n


if __name__ == "__main__":
    # Get input data
    input_data = get_input("inputs/11_input.txt")

    print(f"Part 1: {compute(input_data, 25)}")
    print(f"Part 2: {compute(input_data, 75)}")
