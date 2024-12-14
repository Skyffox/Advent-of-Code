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


def blink(my_dict):
    """Aaa"""
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
def part_one(data_input, nr_blinks):
    """Comment"""
    n = 0
    for num in data_input:
        d = {num : 1}
        for _ in range(nr_blinks):
            d = blink(d)

        n += sum([x[1] for x in d.items()]) # TODO: change to .values()

    return n


if __name__ == "__main__":
    # Get input data
    input_data = get_input("inputs/11_input.txt")

    print(f"Part 1: {part_one(input_data, 25)}")
    print(f"Part 2: {part_one(input_data, 75)}")
