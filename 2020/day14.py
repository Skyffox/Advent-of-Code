# pylint: disable=line-too-long
"""
Day 14: Docking Data

Part 1: Apply a bitmask to values written to memory. Return the sum of all values left in memory.
Answer: 11327140210986

Part 2: Apply a bitmask to memory addresses, generating all possible addresses. Return the sum of values in memory.
Answer: 2308180581795
"""

from typing import List, Dict, Tuple, Union
from utils import profiler


def get_input(file_path: str) -> List[str]:
    """
    Reads the input file and returns a list of stripped lines.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        List[str]: A list of input lines with whitespace removed.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file]


def parse_program(data_input: List[str]) -> List[Tuple[str, Union[str, Tuple[int, int]]]]:
    """
    Parses the raw input into a list of structured instructions.

    Returns:
        List of tuples where:
        - The first element is the instruction type: "mask" or "mem".
        - The second element is either the mask string or a (memory_address, value) tuple.
    """
    program = []
    for line in data_input:
        if line.startswith("mask"):
            mask = line.split(" = ")[1]
            program.append(("mask", mask))
        else:
            left, right = line.split(" = ")
            addr = int(left[left.index("[") + 1:left.index("]")])
            value = int(right)
            program.append(("mem", (addr, value)))
    return program


def apply_mask_to_value(mask: str, value: int) -> int:
    """
    Applies the Part 1 bitmask to a value.

    Args:
        mask (str): The bitmask string.
        value (int): The value to apply the mask to.

    Returns:
        int: The resulting value after the mask is applied.
    """
    bin_value = list(f"{value:036b}")
    for i, bit in enumerate(mask):
        if bit != "X":
            bin_value[i] = bit
    return int("".join(bin_value), 2)


def get_addresses(mask: str, address: int) -> List[int]:
    """
    Applies the Part 2 bitmask to a memory address, generating all floating combinations.

    Args:
        mask (str): The bitmask string.
        address (int): The original memory address.

    Returns:
        List[int]: All resulting addresses after floating bit expansion.
    """
    bin_address = list(f"{address:036b}")
    for i, bit in enumerate(mask):
        if bit == "1":
            bin_address[i] = "1"
        elif bit == "X":
            bin_address[i] = "X"

    addresses = [""]

    for bit in bin_address:
        if bit == "X":
            addresses = [addr + b for addr in addresses for b in "01"]
        else:
            addresses = [addr + bit for addr in addresses]

    return [int(addr, 2) for addr in addresses]


@profiler
def part_one(data_input: List[str]) -> int:
    """
    Executes the initialization program using a bitmask on values before writing to memory.

    The memory is updated based on the mask: 'X' leaves a bit unchanged, '1' and '0' override it.
    After all instructions are processed, the function returns the sum of all values in memory.

    Args:
        data_input (List[str]): List of input lines from the puzzle file.

    Returns:
        int: Sum of all values in memory after completion.
    """
    program = parse_program(data_input)
    mask = ""
    memory: Dict[int, int] = {}

    for instr, val in program:
        if instr == "mask":
            mask = val
        else:
            addr, value = val 
            memory[addr] = apply_mask_to_value(mask, value)

    return sum(memory.values())


@profiler
def part_two(data_input: List[str]) -> int:
    """
    Executes the initialization program using a bitmask on memory addresses (with floating bits).

    The bitmask modifies the address:
    - '0' keeps the original bit
    - '1' overwrites with 1
    - 'X' represents a floating bit (0 or 1)
    
    The value is written to all generated memory addresses. Returns the sum of all values in memory.

    Args:
        data_input (List[str]): List of input lines from the puzzle file.

    Returns:
        int: Sum of all values in memory after completion.
    """
    program = parse_program(data_input)
    mask = ""
    memory: Dict[int, int] = {}

    for instr, val in program:
        if instr == "mask":
            mask = val
        else:
            addr, value = val
            for real_addr in get_addresses(mask, addr):
                memory[real_addr] = value

    return sum(memory.values())


if __name__ == "__main__":
    input_data = get_input("inputs/14_input.txt")
    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
