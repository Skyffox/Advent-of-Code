# pylint: disable=line-too-long
"""
Part 1: Define all possible operations on a list of numbers and see if a combination fits an answer
Answer: 975671981569

Part 2: Do the same as part 1, but there is an additional operator || that concatenates two values
Answer: 223472064194845
"""

import time


def eval_equation(nums: list, target: int) -> bool:
    """Evaluates a list of integers from left to right using + and * operations to find a target."""
    if nums[0] > target:
        return False

    if len(nums) == 1:
        return nums[0] == target

    # Take the first number from the list and do calculations on it
    n = nums.pop(0)

    add = list(nums)
    mul = list(nums)

    add[0] += n
    mul[0] *= n

    return eval_equation(add, target) or eval_equation(mul, target)


def eval_equation_part_2(nums: list, target: int) -> bool:
    """Evaluates a list of integers from left to right using +, * and || operations to find a target."""
    if nums[0] > target:
        return False

    if len(nums) == 1:
        return nums[0] == target

    # Take the first number from the list and do calculations on it
    n = nums.pop(0)

    add = list(nums)
    mul = list(nums)
    concat = list(nums)

    add[0] += n
    mul[0] *= n
    concat[0] = int(str(n) + str(concat[0]))

    return eval_equation_part_2(add, target) or eval_equation_part_2(mul, target) or eval_equation_part_2(concat, target)


def get_input(file_path: str) -> tuple[list, list]:
    """Get the input data"""
    ans, nums = [], []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip().split(":")
            ans.append(int(line[0]))
            nums.append(list(map(int, line[1].strip().split(" "))))

    return ans, nums


if __name__ == "__main__":
    t1 = time.time()

    # Get input data
    answers, numbers = get_input("inputs/7_input.txt")

    total_part_1, total_part_2 = 0, 0
    for answer, number in zip(answers, numbers):
        total_part_1 += answer if eval_equation(number.copy(), answer) else 0
        total_part_2 += answer if eval_equation_part_2(number, answer) else 0

    print(f"Part 1: {total_part_1}")
    print(f"Part 2: {total_part_2}")

    # Calc execution time, not really suited for the profiler since we use recursion
    t2 = time.time()
    print(f"Executed in {t2 - t1:0.4f} seconds")
