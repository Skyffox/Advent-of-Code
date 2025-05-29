# pylint: disable=line-too-long
"""
Day 9: Marble Mania

Part 1: What is the winning Elf's score?
Answer: 384475

Part 2: What would the new winning Elf's score be if the number of the last marble were 100 times larger?
Answer: 335249
"""

from typing import Tuple
from utils import profiler


def get_input(file_path: str) -> Tuple[int, int]:
    """
    Reads the input file and returns the number of players and the last marble value.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        tuple[int, int]: A tuple containing the number of players and the last marble value.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        line = file.readline().strip()
        parts = line.split(" ")
        players = int(parts[0])
        last_marble = int(parts[-2])
        return players, last_marble


class Node:
    """Custom class to implement a doubly-linked list"""
    def __init__(self, value):
        self.value = value
        # Initially, a node points to itself — circular doubly linked list base case
        self.prev = self
        self.next = self


def play_game(players: int, last_marble: int) -> int:
    """
    Simulates the marble game and returns the highest score.

    Args:
        players (int): The number of players.
        last_marble (int): The value of the last marble.

    Returns:
        int: The highest score achieved.
    """
    scores = [0] * players
    current = Node(0)

    for marble in range(1, last_marble + 1):
        player = (marble - 1) % players

        # Special case: The current player adds this marble number PLUS the value of the marble
        # 7 marbles counter-clockwise from the current marble
        if marble % 23 == 0:
            # Move current pointer 7 steps counter-clockwise by following `prev`
            for _ in range(7):
                current = current.prev
            scores[player] += marble + current.value

            # Remove the marble at current position by linking its neighbors
            current.prev.next = current.next
            current.next.prev = current.prev
            # Set current to the marble immediately clockwise of the removed marble
            current = current.next
        else:
            # Normal case: Insert new marble between the marbles that are 1 and 2 positions clockwise from current
            # The marble will be inserted between current.next and current.next.next
            node = Node(marble)
            after = current.next.next
            before = current.next
            # Insert the new node between 'before' and 'after'
            before.next = node
            node.prev = before
            node.next = after
            after.prev = node
            # The newly inserted marble becomes the current marble
            current = node

    return max(scores)


@profiler
def part_one(players: int, last_marble: int) -> int:
    """
    Solves part one of the problem using the provided input data.

    Args:
        players int: amount of players in the game
        last_marble int: value of the last marble

    Returns:
        int: The highest score achieved.
    """
    return play_game(players, last_marble)


@profiler
def part_two(players: int, last_marble: int) -> int:
    """
    Solves part two of the problem using the provided input data.

    Args:
        data_input (List[str]): A list of input lines from the puzzle input file.

    Returns:
        int: The highest score achieved with 100 times the last marble value.
    """
    return play_game(players, last_marble * 100)


if __name__ == "__main__":
    play, marb = get_input("inputs/9_input.txt")

    print(f"Part 1: {part_one(play, marb)}")
    print(f"Part 2: {part_two(play, marb)}")
