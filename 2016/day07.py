# pylint: disable=line-too-long
"""
Day 7: Internet Protocol Version 7

Part 1: How many IPs in your puzzle input support TLS?
Answer: 110

Part 2: How many IPs in your puzzle input support SSL?
Answer: 242
"""

from typing import List
import re
from utils import profiler


def get_input(file_path: str) -> List[str]:
    """
    Reads the input file and returns a list of stripped lines.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        list[str]: List of input lines.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file]


def has_abba(s: str) -> bool:
    """
    Returns True if the string contains an ABBA sequence (xyyx) where x != y.

    Args:
        s (str): Input string.

    Returns:
        bool: True if ABBA found, else False.
    """
    for i in range(len(s) - 3):
        segment = s[i:i+4]
        if segment[0] != segment[1] and segment == segment[::-1]:
            return True
    return False


def supports_tls(ip: str) -> bool:
    """
    Determines if an IP supports TLS (Transport-Layer Snooping).

    Args:
        ip (str): The IP string.

    Returns:
        bool: True if supports TLS, False otherwise.
    """
    # Split into supernet (outside []) and hypernet (inside [])
    parts = re.split(r'(\[.*?\])', ip)
    supernets = []
    hypernets = []
    for part in parts:
        if part.startswith('[') and part.endswith(']'):
            hypernets.append(part[1:-1])
        else:
            supernets.append(part)

    # Check hypernets for ABBA (if any hypernet has ABBA, no TLS)
    if any(has_abba(h) for h in hypernets):
        return False

    # Check supernets for at least one ABBA
    return any(has_abba(s) for s in supernets)


def get_aba(s: str) -> List[str]:
    """
    Returns all ABA sequences in the string.

    Args:
        s (str): Input string.

    Returns:
        List[str]: List of ABA substrings.
    """
    aba_list = []
    for i in range(len(s) - 2):
        segment = s[i : i + 3]
        if segment[0] == segment[2] and segment[0] != segment[1]:
            aba_list.append(segment)
    return aba_list


def supports_ssl(ip: str) -> bool:
    """
    Determines if an IP supports SSL (Super-Secret Listening).

    Args:
        ip (str): The IP string.

    Returns:
        bool: True if supports SSL, False otherwise.
    """
    parts = re.split(r'(\[.*?\])', ip)
    supernets = []
    hypernets = []
    for part in parts:
        if part.startswith('[') and part.endswith(']'):
            hypernets.append(part[1:-1])
        else:
            supernets.append(part)

    aba_sequences = []
    for supernet in supernets:
        aba_sequences.extend(get_aba(supernet))

    # For each ABA, check if corresponding BAB exists in any hypernet
    for aba in aba_sequences:
        bab = aba[1] + aba[0] + aba[1]
        if any(bab in h for h in hypernets):
            return True
    return False


@profiler
def part_one(data_input: List[str]) -> int:
    """
    Counts IPs that support TLS.

    Args:
        data_input (List[str]): List of IP strings.

    Returns:
        int: Number of IPs supporting TLS.
    """
    return sum(supports_tls(ip) for ip in data_input)


@profiler
def part_two(data_input: List[str]) -> int:
    """
    Counts IPs that support SSL.

    Args:
        data_input (List[str]): List of IP strings.

    Returns:
        int: Number of IPs supporting SSL.
    """
    return sum(supports_ssl(ip) for ip in data_input)


if __name__ == "__main__":
    input_data = get_input("inputs/7_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
