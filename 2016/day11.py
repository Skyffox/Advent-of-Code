# pylint: disable=line-too-long
"""
Day 11: Radioisotope Thermoelectric Generators

Part 1: In your situation, what is the minimum number of steps required to bring all of the objects to the fourth floor?
Answer: 31

Part 2: What is the minimum number of steps required to bring all of the objects, including these four new ones, to the fourth floor?
Answer: 71
"""

from itertools import chain, combinations
from typing import List, Set, Tuple
from collections import Counter, deque
from utils import profiler

Floor = Set[Tuple[str, str]]  # Each floor is a set of (element, type) tuples.
State = Tuple[int, int, List[Floor]]  # (moves, elevator position, floor configuration)


def get_input(file_path: str) -> List[Floor]:
    """
    Reads the input file and returns a list of stripped lines.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        list[str]: List of input lines.
    """
    initial_floors  = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            floor = set()
            words = line.lower().replace(',', '').replace('.', '').split()
            for idx, word in enumerate(words):
                if word.endswith('generator'):
                    floor.add((words[idx - 1], "generator"))
                elif word.endswith('microchip'):
                    floor.add((words[idx - 1].split("-")[0], "microchip"))
            initial_floors.append(floor)

    return initial_floors


def is_valid_transition(floor: Floor) -> bool:
    """
    Checks whether a given floor configuration is safe.

    Args:
        floor (Floor): Set of items on the floor.

    Returns:
        bool: True if the configuration is safe, False otherwise.
    """
    return (
        len(set(type for _, type in floor)) < 2 or
        all((obj, 'generator') in floor for (obj, type) in floor if type == 'microchip')
    )


def next_states(state: State):
    """
    Generates all valid next states from the current state.

    Args:
        state (State): Current (moves, elevator_position, floors)

    Yields:
        State: Next valid state after a legal move.
    """
    moves, elevator, floors = state

    possible_moves = chain(combinations(floors[elevator], 2), combinations(floors[elevator], 1))

    for move in possible_moves:
        for direction in [-1, 1]:
            next_elevator = elevator + direction
            if not 0 <= next_elevator < len(floors):
                continue

            next_floors = floors.copy()
            next_floors[elevator] = next_floors[elevator].difference(move)
            next_floors[next_elevator] = next_floors[next_elevator].union(move)

            if (is_valid_transition(next_floors[elevator]) and is_valid_transition(next_floors[next_elevator])):
                yield (moves + 1, next_elevator, next_floors)


def count_floor_objects(state: State):
    """
    Normalizes a state to reduce equivalent states by counting item types on each floor.

    Args:
        state (State): The current state (moves, elevator_position, floors)

    Returns:
        tuple: A tuple used as a hashable key for visited state deduplication.
    """
    _, elevator, floors = state
    return elevator, tuple(
        tuple(Counter(type for _, type in floor).most_common())
        for floor in floors
    )


@profiler
def compute(floors: List[Floor], is_part2: bool) -> int:
    """
    Computes the minimum number of steps required to move all items to the top floor.

    Args:
        floors (List[Floor]): Initial configuration of items on each floor.
        is_part2 (bool): Whether to use the extended input for Part 2.

    Returns:
        int: Minimum number of steps to bring all items to the top floor.
    """
    queue = deque([(0, 0, floors)]) # moves, elevator, floors
    visited = set()

    if is_part2:
        floors[0] = floors[0].union([('elerium', 'generator'), ('elerium', 'microchip'), ('dilithium', 'generator'), ('dilithium', 'microchip')])

    while queue:
        state = queue.popleft()
        moves, _, floors = state

        # Check if all items on top floor
        if all(not floor for number, floor in enumerate(floors) if number < len(floors) - 1):
            return moves

        for next_state in next_states(state):
            if (key := count_floor_objects(next_state)) not in visited:
                visited.add(key)
                queue.append(next_state)

    return -1 # Not found


if __name__ == "__main__":
    input_data = get_input("inputs/11_input.txt")

    print(f"Part 1: {compute(input_data, False)}")
    print(f"Part 2: {compute(input_data, True)}")
