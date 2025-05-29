# pylint: disable=line-too-long
"""
Day 10: Syntax Scoring

Part 1: Find the first illegal character in each corrupted line of the navigation subsystem. What is the total syntax error score for those errors?
Answer: 442131

Part 2: Find the completion string for each incomplete line, score the completion strings, and sort the scores. What is the middle score?
Answer: 3646451424
"""

from typing import List
from utils import profiler


def get_input(file_path: str) -> List[str]:
    """
    Reads the input file and returns a list of chunk lines.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        List[str]: List of chunk strings.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file.readlines()]


# Mapping for chunk pairs
PAIRS = {"(": ")", "[": "]", "{": "}", "<": ">"}

# Syntax error scores for corrupted lines
SYNTAX_ERROR_SCORES = {")": 3, "]": 57, "}": 1197, ">": 25137}

# Completion scores for incomplete lines
COMPLETION_SCORES = {")": 1, "]": 2, "}": 3, ">": 4}


@profiler
def part_one(lines: List[str]) -> int:
    """
    Calculates total syntax error score for corrupted lines.

    Args:
        lines (List[str]): List of chunk lines.

    Returns:
        int: Total syntax error score.
    """
    total_score = 0
    for line in lines:
        stack = []
        for char in line:
            if char in PAIRS:
                stack.append(char)
            else:
                if not stack:
                    total_score += SYNTAX_ERROR_SCORES[char]
                    break
                last = stack.pop()
                if PAIRS[last] != char:
                    total_score += SYNTAX_ERROR_SCORES[char]
                    break
    return total_score


@profiler
def part_two(lines: List[str]) -> int:
    """
    Calculates the middle score of completion strings for incomplete lines.

    Args:
        lines (List[str]): List of chunk lines.

    Returns:
        int: Middle completion score.
    """
    completion_scores = []

    for line in lines:
        stack = []
        corrupted = False
        for char in line:
            if char in PAIRS:
                stack.append(char)
            else:
                if not stack:
                    corrupted = True
                    break
                last = stack.pop()
                if PAIRS[last] != char:
                    corrupted = True
                    break
        if not corrupted and stack:
            score = 0
            while stack:
                last = stack.pop()
                score = score * 5 + COMPLETION_SCORES[PAIRS[last]]
            completion_scores.append(score)

    completion_scores.sort()
    return completion_scores[len(completion_scores) // 2]


if __name__ == "__main__":
    input_data = get_input("inputs/10_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
