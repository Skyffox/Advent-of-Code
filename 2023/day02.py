# pylint: disable=line-too-long
"""
Part 1: See if the game is valid by comparing pulled cubes with set maximum
Answer: 2285

Part 2: See what the maximum amount of cubes is needed to play every game
Answer: 77021
"""

from utils import profiler


def get_input(file_path: str) -> list:
    """Get the input data"""
    data = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip().split(":")
            # Separates the game number from the input
            game = line[0].split(" ")[1]

            # Get a tuple of each number and color which is every instruction for the game
            game_input = [
                (int(num), color)
                for part in line[1].split(";")
                for num, color in (item.split() for item in part.strip().split(","))
            ]

            data.append((game, game_input))

    return data


@profiler
def part_1(games: list) -> int:
    """See if inputs lie within the allowed maximum"""
    n = 0
    maximums = {'red' : 12, 'green' : 13, 'blue' : 14}

    for game in games:
        valid_input = True
        game_number, game_inputs = game
        for num, color in game_inputs:
            if int(num > maximums[color]):
                valid_input = False
                break

        if valid_input:
            n += int(game_number)

    return n


@profiler
def part_2(games: list) -> int:
    """t"""
    n = 0

    for game in games:
        max_red, max_green, max_blue = 0, 0, 0
        _, game_inputs = game
        for num, color in game_inputs:
            if color == 'red':
                max_red = max(max_red, num)
            if color == 'green':
                max_green = max(max_green, num)
            if color == 'blue':
                max_blue = max(max_blue, num)

        n += (max_red * max_green * max_blue)

    return n


if __name__ == "__main__":
    input_data = get_input("inputs/2_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
