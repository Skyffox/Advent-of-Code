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


def load_and_parse_program(file_path: str) -> List[Tuple[str, Union[str, Tuple[int, int]]]]:
    """
    Reads the input file and parses it into a structured program list.

    Each element is a tuple:
      - ("mask", mask_str) or
      - ("mem", (address, value))

    Args:
        file_path (str): Path to the input text file.

    Returns:
        List[Tuple[str, Union[str, Tuple[int, int]]]]: Parsed instructions.
    """
    program = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
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
def run_program(program: List[Tuple[str, Union[str, Tuple[int, int]]]], part: int) -> int:
    """
    Executes the initialization program according to the specified part's rules.

    Part 1:
      - Applies bitmask to values before writing to memory.

    Part 2:
      - Applies bitmask to memory addresses (floating bits), writing values to all resulting addresses.

    Args:
        program (List[Tuple[str, Union[str, Tuple[int, int]]]]): Parsed instructions.
        part (int): 1 or 2, to select which behavior to run.

    Returns:
        int: Sum of all values left in memory after program completion.
    """
    mask = ""
    memory: Dict[int, int] = {}

    for instr, val in program:
        if instr == "mask":
            mask = val
        else:
            addr, value = val
            if part == 1:
                memory[addr] = apply_mask_to_value(mask, value)
            elif part == 2:
                for real_addr in get_addresses(mask, addr):
                    memory[real_addr] = value

    return sum(memory.values())


if __name__ == "__main__":
    input_data = load_and_parse_program("inputs/14_input.txt")

    print(f"Part 1: {run_program(input_data, part=1)}")
    print(f"Part 2: {run_program(input_data, part=2)}")
