# pylint: disable=line-too-long
"""
Day 8: Seven Segment Search

Part 1: In the output values, how many times do digits 1, 4, 7, or 8 appear?
Answer: 272

Part 2: For each entry, determine all of the wire/segment connections and decode the four-digit output values. 
        What do you get if you add up all of the output values?
Answer: 1007675
"""

from typing import List, Tuple
from utils import profiler


def get_input(file_path: str) -> List[Tuple[List[str], List[str]]]:
    """
    Reads the input file and returns a list of tuples with signal patterns and output values.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        List of tuples: (signal_patterns, output_values), each a list of strings.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.read().strip().split("\n")
        entries = []
        for line in lines:
            signals, outputs = line.split(" | ")
            entries.append((signals.split(), outputs.split()))
        return entries


@profiler
def part_one(data_input: List[Tuple[List[str], List[str]]]) -> int:
    """
    Counts the number of times digits with unique segment counts appear in the output.

    Digits with unique segment lengths:
    - 1 (2 segments)
    - 4 (4 segments)
    - 7 (3 segments)
    - 8 (7 segments)

    Args:
        data_input (List[Tuple[List[str], List[str]]]): Input entries.

    Returns:
        int: Count of unique segment digits in outputs.
    """
    unique_lengths = {2, 3, 4, 7}
    count = 0
    for _, output_values in data_input:
        count += sum(len(digit) in unique_lengths for digit in output_values)
    return count


def decode_line(signal_patterns: List[str], output_values: List[str]) -> int:
    """
    Decodes a single line's output value based on the signal patterns.

    Args:
        signal_patterns (List[str]): The ten unique signal patterns.
        output_values (List[str]): The four output digits to decode.

    Returns:
        int: The decoded output number.
    """
    patterns = [''.join(sorted(p)) for p in signal_patterns]
    outputs = [''.join(sorted(o)) for o in output_values]

    # Map from pattern string to digit
    digit_map = {}

    # First find digits with unique lengths: 1, 4, 7, 8
    for p in patterns:
        if len(p) == 2:
            digit_map[1] = p
        elif len(p) == 4:
            digit_map[4] = p
        elif len(p) == 3:
            digit_map[7] = p
        elif len(p) == 7:
            digit_map[8] = p

    # Helper function to count overlap
    def overlap(a: str, b: str) -> int:
        return len(set(a) & set(b))

    # Identify digits of length 6: 0, 6, 9
    six_len = [p for p in patterns if len(p) == 6]
    for p in six_len:
        if overlap(p, digit_map[4]) == 4:
            digit_map[9] = p
        elif overlap(p, digit_map[1]) == 2:
            digit_map[0] = p
        else:
            digit_map[6] = p

    # Identify digits of length 5: 2, 3, 5
    five_len = [p for p in patterns if len(p) == 5]
    for p in five_len:
        if overlap(p, digit_map[1]) == 2:
            digit_map[3] = p
        elif overlap(p, digit_map[4]) == 3:
            digit_map[5] = p
        else:
            digit_map[2] = p

    # Reverse the mapping for decoding
    rev_map = {v: k for k, v in digit_map.items()}

    # Decode output values
    decoded_digits = [str(rev_map[o]) for o in outputs]
    return int(''.join(decoded_digits))


@profiler
def part_two(data_input: List[Tuple[List[str], List[str]]]) -> int:
    """
    Decodes all output values and sums them.

    Args:
        data_input (List[Tuple[List[str], List[str]]]): Input entries.

    Returns:
        int: Sum of all decoded output numbers.
    """
    return sum(decode_line(signals, outputs) for signals, outputs in data_input)


if __name__ == "__main__":
    input_data = get_input("inputs/8_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
