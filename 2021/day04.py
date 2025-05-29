# pylint: disable=line-too-long
"""
Day 4: Giant Squid

Part 1: To guarantee victory against the giant squid, figure out which board will win first. What will your final score be if you choose that board?
Answer: 11536

Part 2: Figure out which board will win last. Once it wins, what would its final score be?
Answer: 1284
"""

from typing import List, Tuple
from utils import profiler


def get_input(file_path: str) -> Tuple[List[int], List[List[List[int]]]]:
    """
    Reads the input file and returns the drawn numbers and the list of bingo boards.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        Tuple containing:
            - drawn_numbers (List[int]): The sequence of numbers drawn.
            - boards (List[List[List[int]]]): List of boards, each a 2D list of integers.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read().strip().split("\n\n")
        drawn_numbers = list(map(int, content[0].split(",")))
        boards = []
        for board_str in content[1:]:
            board = [list(map(int, line.split())) for line in board_str.split("\n")]
            boards.append(board)
        return drawn_numbers, boards


def mark_number(board: List[List[int]], number: int) -> None:
    """
    Marks the number on the board by setting it to -1.

    Args:
        board (List[List[int]]): The bingo board.
        number (int): The number to mark.
    """
    for i in range(5):
        for j in range(5):
            if board[i][j] == number:
                board[i][j] = -1


def has_won(board: List[List[int]]) -> bool:
    """
    Checks if the board has won (a full row or column marked).

    Args:
        board (List[List[int]]): The bingo board.

    Returns:
        bool: True if board has won, False otherwise.
    """
    for i in range(5):
        if all(cell == -1 for cell in board[i]): # check row
            return True
        if all(board[j][i] == -1 for j in range(5)): # check column
            return True
    return False


def score(board: List[List[int]], last_number: int) -> int:
    """
    Calculates the score of the winning board.

    Args:
        board (List[List[int]]): The bingo board.
        last_number (int): The last number called.

    Returns:
        int: The score.
    """
    unmarked_sum = sum(cell for row in board for cell in row if cell != -1)
    return unmarked_sum * last_number


@profiler
def part_one(data_input: Tuple[List[int], List[List[List[int]]]]) -> int:
    """
    Finds the score of the first winning board.

    Args:
        data_input (Tuple[List[int], List[List[List[int]]]]): Drawn numbers and boards.

    Returns:
        int: Score of the first winning board.
    """
    drawn_numbers, boards = data_input
    for number in drawn_numbers:
        for board in boards:
            mark_number(board, number)
            if has_won(board):
                return score(board, number)
    return 0


@profiler
def part_two(data_input: Tuple[List[int], List[List[List[int]]]]) -> int:
    """
    Finds the score of the last winning board.

    Args:
        data_input (Tuple[List[int], List[List[List[int]]]]): Drawn numbers and boards.

    Returns:
        int: Score of the last winning board.
    """
    drawn_numbers, boards = data_input
    won_boards = set()
    last_score = 0

    for number in drawn_numbers:
        for idx, board in enumerate(boards):
            if idx in won_boards:
                continue
            mark_number(board, number)
            if has_won(board):
                won_boards.add(idx)
                last_score = score(board, number)
        if len(won_boards) == len(boards):
            break
    return last_score


if __name__ == "__main__":
    input_data = get_input("inputs/4_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
