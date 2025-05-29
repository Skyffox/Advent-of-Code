# pylint: disable=line-too-long
"""
Day 4: Security Through Obscurity

Part 1: What is the sum of the sector IDs of the real rooms?
Answer: 245102

Part 2: What is the sector ID of the room where North Pole objects are stored?
Answer: 324
"""

from typing import List
import re
from collections import Counter
from utils import profiler


def get_input(file_path: str) -> List[str]:
    """
    Reads the input file and returns a list of stripped lines.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        list[str]: A list of lines with leading/trailing whitespace removed.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file]


def is_real_room(name: str, checksum: str) -> bool:
    """
    Determines if a room is real by comparing its checksum with letter frequency.

    Args:
        name (str): Encrypted room name (dashes included).
        checksum (str): Checksum string.

    Returns:
        bool: True if real room, False otherwise.
    """
    name = name.replace("-", "")
    counts = Counter(name)
    # Sort by frequency (desc), then alphabetically (asc)
    sorted_letters = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
    calculated_checksum = "".join(letter for letter, _ in sorted_letters[:5])
    return calculated_checksum == checksum


def decrypt_name(name: str, sector_id: int) -> str:
    """
    Decrypts the room name by rotating letters forward sector_id times.

    Args:
        name (str): Encrypted room name with dashes.
        sector_id (int): Sector ID used as rotation amount.

    Returns:
        str: Decrypted room name with spaces instead of dashes.
    """
    decrypted = []
    for char in name:
        if char == "-":
            decrypted.append(" ")
        else:
            shifted = chr(((ord(char) - ord('a') + sector_id) % 26) + ord('a'))
            decrypted.append(shifted)
    return "".join(decrypted)


@profiler
def part_one(data_input: List[str]) -> int:
    """
    Sum sector IDs of real rooms.

    Args:
        data_input (List[str]): List of input lines.

    Returns:
        int: Sum of sector IDs of real rooms.
    """
    total = 0
    pattern = re.compile(r"([a-z-]+)-(\d+)\[([a-z]+)\]")
    for line in data_input:
        match = pattern.match(line)
        if not match:
            continue
        name, sector_id_str, checksum = match.groups()
        sector_id = int(sector_id_str)
        if is_real_room(name, checksum):
            total += sector_id
    return total


@profiler
def part_two(data_input: List[str]) -> int:
    """
    Finds the sector ID of the room where the decrypted name contains 'northpole'.

    Args:
        data_input (List[str]): List of input lines.

    Returns:
        int: Sector ID of the North Pole object storage room.
    """
    pattern = re.compile(r"([a-z-]+)-(\d+)\[([a-z]+)\]")
    for line in data_input:
        match = pattern.match(line)
        if not match:
            continue
        name, sector_id_str, checksum = match.groups()
        sector_id = int(sector_id_str)
        if is_real_room(name, checksum):
            decrypted = decrypt_name(name, sector_id)
            if "northpole" in decrypted:
                return sector_id
    return -1


if __name__ == "__main__":
    input_data = get_input("inputs/4_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
