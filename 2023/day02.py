# pylint: disable=line-too-long
"""
Day 2: Cube Conundrum

Part 1: See if the game is valid by comparing pulled cubes with set maximum
Answer: 2285

Part 2: See what the maximum amount of cubes is needed to play every game
Answer: 77021
"""

from typing import List, Tuple
from utils import profiler


def get_input(file_path: str) -> List[Tuple[str, List[Tuple[int, str]]]]:
    """
    Parse the input file and return game data.
    Each game consists of a game number and a list of (number, color) tuples representing cube pulls.

    Args:
        file_path (str): Path to the input file.

    Returns:
        List[Tuple[str, List[Tuple[int, str]]]]: Parsed game data.
    """
    data = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip().split(":")
            game = line[0].split(" ")[1]

            # Extract all cube draws as (number, color) tuples
            game_input = [
                (int(num), color)
                for part in line[1].split(";")
                for num, color in (item.split() for item in part.strip().split(","))
            ]

            data.append((game, game_input))

    return data


@profiler
def part_1(games: List[Tuple[str, List[Tuple[int, str]]]]) -> int:
    """
    Determine the sum of game numbers where all cube pulls are within allowed limits.

    Args:
        games (List[Tuple[str, List[Tuple[int, str]]]]): List of games with cube pull details.

    Returns:
        int: Sum of valid game numbers.
    """
    total = 0
    maximums = {'red': 12, 'green': 13, 'blue': 14}

    for game_number, game_inputs in games:
        if all(num <= maximums[color] for num, color in game_inputs):
            total += int(game_number)

    return total


@profiler
def part_2(games: List[Tuple[str, List[Tuple[int, str]]]]) -> int:
    """
    For each game, compute the product of the maximum required red, green, and blue cubes.
    Sum these products over all games.

    Args:
        games (List[Tuple[str, List[Tuple[int, str]]]]): List of games with cube pull details.

    Returns:
        int: Sum of cube set products for all games.
    """
    total = 0

    for _, game_inputs in games:
        max_red, max_green, max_blue = 0, 0, 0
        for num, color in game_inputs:
            if color == 'red':
                max_red = max(max_red, num)
            elif color == 'green':
                max_green = max(max_green, num)
            elif color == 'blue':
                max_blue = max(max_blue, num)

        total += max_red * max_green * max_blue

    return total


if __name__ == "__main__":
    input_data = get_input("inputs/2_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
