# pylint: disable=line-too-long
"""
Day 16: Permutation Promenade

Part 1: You watch the dance for a while and record their dance moves (your puzzle input). In what order are the programs standing after their dance?
Answer: gkmndaholjbfcepi

Part 2: In what order are the programs standing after their billion dances?
Answer: abihnfkojcmegldp
"""

from typing import List
from utils import profiler


def get_input(file_path: str) -> List[str]:
    """
    Reads the input file and returns list of dance moves.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        List[str]: List of moves as strings.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        line = file.readline().strip()
        return line.split(',')


def dance(moves: List[str], programs: List[str]) -> List[str]:
    """
    Performs a sequence of dance moves on programs.

    Args:
        moves (List[str]): List of moves.
        programs (List[str]): Current order of programs.

    Returns:
        List[str]: Programs after dance moves.
    """
    for move in moves:
        if move[0] == 's':  # spin
            x = int(move[1:])
            programs = programs[-x:] + programs[:-x]
        elif move[0] == 'x':  # exchange
            a, b = map(int, move[1:].split('/'))
            programs[a], programs[b] = programs[b], programs[a]
        elif move[0] == 'p':  # partner
            a, b = move[1:].split('/')
            ia, ib = programs.index(a), programs.index(b)
            programs[ia], programs[ib] = programs[ib], programs[ia]
    return programs


@profiler
def part_one(data_input: List[str]) -> str:
    """
    Runs the dance moves once.

    Args:
        data_input (List[str]): List of dance moves.

    Returns:
        str: Final order of programs.
    """
    programs = list("abcdefghijklmnop")
    programs = dance(data_input, programs)
    return ''.join(programs)


@profiler
def part_two(data_input: List[str]) -> str:
    """
    Runs the dance moves one billion times, using cycle detection.

    Args:
        data_input (List[str]): List of dance moves.

    Returns:
        str: Final order of programs.
    """
    programs = list("abcdefghijklmnop")
    seen = []
    for i in range(1_000_000_000):
        programs = dance(data_input, programs)
        s = ''.join(programs)
        if s in seen:
            # Cycle detected, skip ahead
            cycle_start = seen.index(s)
            cycle_length = i - cycle_start
            remaining = (1_000_000_000 - i - 1) % cycle_length
            return seen[cycle_start + remaining]
        seen.append(s)
    return ''.join(programs)


if __name__ == "__main__":
    input_data = get_input("inputs/16_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
