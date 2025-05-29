# pylint: disable=line-too-long
"""
Day 7: The Sum of Its Parts

Part 1: In what order should the steps in your instructions be completed?
Answer: BKCJMSDVGHQRXFYZOAULPIEWTN

Part 2: With 5 workers and the 60+ second step durations described above, how long will it take to complete all of the steps?
Answer: 1040
"""

from typing import Dict, List, Set, Tuple
from collections import defaultdict, deque
import re
from utils import profiler


def get_input(file_path: str) -> List[Tuple[str, str]]:
    """
    Parses the input file and extracts all step dependencies.

    Each line describes a dependency of the form:
    "Step C must be finished before step A can begin."

    Args:
        filename (str): Path to the input file.

    Returns:
        List[Tuple[str, str]]: A list of (prerequisite, step) pairs.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [re.findall(r"Step (\w).*step (\w)", line)[0] for line in file]


def build_graph(instructions: List[Tuple[str, str]]) -> Tuple[Dict[str, List[str]], Dict[str, int], Set[str]]:
    """
    Builds a directed graph and computes in-degrees for each step.

    Args:
        instructions (List[Tuple[str, str]]): List of (prerequisite, step) pairs.

    Returns:
        Tuple containing:
            - graph (Dict[str, List[str]]): Adjacency list of the graph.
            - in_degree (Dict[str, int]): Number of prerequisites for each step.
            - all_steps (Set[str]): Set of all steps involved.
    """
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    all_steps = set()

    for before, after in instructions:
        graph[before].append(after)
        in_degree[after] += 1
        all_steps.update([before, after])

    # Ensure all steps have an entry in in_degree
    for step in all_steps:
        in_degree.setdefault(step, 0)

    return graph, in_degree, all_steps


@profiler
def part_one(instructions: List[Tuple[str, str]]) -> str:
    """
    Solves Part 1 of the problem: finds the correct order of steps.

    Steps must be performed in order respecting dependencies. 
    When multiple steps are available, the alphabetically first is chosen.

    Args:
        instructions (List[Tuple[str, str]]): Step dependencies.

    Returns:
        str: The ordered sequence of steps as a string.
    """
    graph, in_degree, _ = build_graph(instructions)
    order = []
    queue = deque(sorted([step for step, degree in in_degree.items() if degree == 0]))

    while queue:
        current = queue.popleft()
        order.append(current)

        for neighbor in graph[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

        queue = deque(sorted(queue))  # Keep lexicographical order

    return ''.join(order)


@profiler
def part_two(instructions: List[Tuple[str, str]], num_workers: int = 5, base_duration: int = 60) -> int:
    """
    Solves Part 2: Simulates workers completing steps with varying durations.

    Each step takes a duration of base_duration + (A=1 ... Z=26).
    Workers can only start a step if all prerequisites are complete.

    Args:
        instructions (List[Tuple[str, str]]): Step dependencies.
        num_workers (int): Number of workers available.
        base_duration (int): Base duration to add to step value.

    Returns:
        int: Total time required to complete all steps.
    """
    graph, in_degree, all_steps = build_graph(instructions)
    time = 0
    workers: List[Tuple[str, int]] = []  # (step, finish_time)
    in_progress: Set[str] = set()
    completed: Set[str] = set()

    while len(completed) < len(all_steps):
        # Assign available steps to available workers
        available_steps = sorted(
            step for step in all_steps
            if in_degree[step] == 0 and step not in in_progress and step not in completed
        )

        while len(workers) < num_workers and available_steps:
            step = available_steps.pop(0)
            duration = base_duration + ord(step) - ord('A') + 1
            workers.append((step, time + duration))
            in_progress.add(step)

        # Advance time to next task completion
        next_completion = min(finish for _, finish in workers)
        time = next_completion

        # Complete all tasks finishing at this time
        finished = [step for step, finish in workers if finish == time]
        workers = [(step, finish) for step, finish in workers if finish != time]

        for step in finished:
            completed.add(step)
            in_progress.remove(step)
            for neighbor in graph[step]:
                in_degree[neighbor] -= 1

    return time


if __name__ == "__main__":
    input_data = get_input("inputs/7_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
