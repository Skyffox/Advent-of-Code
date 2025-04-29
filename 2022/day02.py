# pylint: disable=line-too-long
"""
Part 1: What would your total score be if everything goes exactly according to your strategy guide?
Answer: 11666

Part 2: Following the Elf's instructions for the second column, what would your total score be if everything goes exactly according to your strategy guide?
Answer: 12767
"""

from utils import profiler


def get_input(file_path: str) -> list:
    """Get the input data"""
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip().split(" ") for line in file]


@profiler
def part_1(matches: list) -> int:
    """a"""
    score = 0
    for (enemy, player) in matches:
        if enemy == "A":
            if player == "X":
                score += 4
            if player == "Y":
                score += 8
            if player == "Z":
                score += 3

        if enemy == "B":
            if player == "X":
                score += 1
            if player == "Y":
                score += 5
            if player == "Z":
                score += 9

        if enemy == "C":
            if player == "X":
                score += 7
            if player == "Y":
                score += 2
            if player == "Z":
                score += 6

    return score


@profiler
def part_2(matches: list) -> int:
    """a"""
    score = 0
    for (enemy, outcome) in matches:
        if enemy == "A":
            if outcome == "X":
                score += 3
            if outcome == "Y":
                score += 4
            if outcome == "Z":
                score += 8

        if enemy == "B":
            if outcome == "X":
                score += 1
            if outcome == "Y":
                score += 5
            if outcome == "Z":
                score += 9

        if enemy == "C":
            if outcome == "X":
                score += 2
            if outcome == "Y":
                score += 6
            if outcome == "Z":
                score += 7

    return score


if __name__ == "__main__":
    input_data = get_input("inputs/2_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
