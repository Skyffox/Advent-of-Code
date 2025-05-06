# pylint: disable=line-too-long
"""
Day 9: Mirage Maintenance

Part 1: Find the sum of extrapolated values that would come next in the series.
Answer: 2043677056

Part 2: Find the sum of extrapolated values that would precede the series.
Answer: 1062
"""

from utils import profiler


def get_input(file_path: str) -> list:
    """
    Reads the input data from a file and converts it into a list of integer lists.

    Each line in the file is expected to contain a series of space-separated integers. 
    This function splits each line by spaces, converts each value to an integer, and stores 
    all the lines as lists of integers.

    Args:
        file_path (str): The path to the input file containing the series.

    Returns:
        list: A list of lists, where each inner list contains integers parsed from a line in the file.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [list(map(int, line.strip().split(" "))) for line in file]


def differences(lst: list) -> list:
    """
    Calculates the differences between consecutive elements in a list.

    Given a list of integers, this function returns a new list where each element is the difference 
    between the corresponding elements in the input list (i.e., the difference between consecutive 
    elements).

    Args:
        lst (list): A list of integers to calculate differences from.

    Returns:
        list: A list containing the differences between consecutive elements in the input list.
    """
    return [lst[i+1] - lst[i] for i, _ in enumerate(lst) if i != len(lst) - 1]


@profiler
def compute(lst: list) -> tuple:
    """
    Computes the sum of extrapolated values that would come next in the series (Part 1) and 
    the sum of values that would precede the series (Part 2).

    The function takes a list of sequences, where each sequence is a list of integers. For each 
    sequence, it repeatedly calculates the differences between consecutive numbers until the differences 
    are constant. Then, it extrapolates the next and previous values in the sequence based on these differences.

    The final sum of extrapolated values for each sequence is returned as the result for both parts of the problem.

    Args:
        lst (list): A list of sequences, where each sequence is a list of integers.

    Returns:
        tuple: A tuple containing two integers:
            - The first integer is the sum of the extrapolated next values (Part 1).
            - The second integer is the sum of the extrapolated previous values (Part 2).
    """
    total_part1, total_part2 = 0, 0

    for line in lst:
        line_inputs = [line]

        # Repeatedly calculate the differences between consecutive elements in the sequence
        lst = differences(line)
        while lst != [0] * (len(line_inputs[-1]) - 1):
            line_inputs.append(lst)
            lst = differences(line_inputs[-1])

        # Calculate the next value in the sequence by adding the last calculated difference
        diff = 0
        for i in range(len(line_inputs) - 1, -1, -1):
            line_inputs[i].append(line_inputs[i][-1] + diff)
            diff = line_inputs[i][-1]

        # Calculate the previous value in the sequence by subtracting the differences
        diff = 0
        for i in range(len(line_inputs) - 1, -1, -1):
            line_inputs[i].insert(0, line_inputs[i][0] - diff)
            diff = line_inputs[i][0]

        # Add the last extrapolated value and the first extrapolated value to the totals
        total_part1 += line_inputs[0][-1]
        total_part2 += line_inputs[0][0]

    return total_part1, total_part2


if __name__ == "__main__":
    input_data = get_input("inputs/9_input.txt")

    ans_part1, ans_part2 = compute(input_data)

    print(f"Part 1: {ans_part1}")
    print(f"Part 2: {ans_part2}")
