# pylint: disable=line-too-long
"""
Day 12: Passage Pathing

Part 1: How many paths through this cave system are there that visit small caves at most once?
Answer: 3563

Part 2: Given these new rules, how many paths through this cave system are there?
Answer: 105453
"""

from typing import List, Dict, Set


def get_input(file_path: str) -> Dict[str, List[str]]:
    """
    Reads the input file and returns the graph as adjacency list.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        Dict[str, List[str]]: Graph adjacency list.
    """
    graph: Dict[str, List[str]] = {}
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            a, b = line.strip().split("-")
            graph.setdefault(a, []).append(b)
            graph.setdefault(b, []).append(a)
    return graph


def dfs_part_one(graph: Dict[str, List[str]], current: str, visited: Set[str]) -> int:
    """
    DFS traversal counting all paths from start to end (Part 1 rules).

    Rules:
    - The input describes an undirected graph where nodes are caves.
    - Caves are connected by paths (e.g., "start-A", "A-b").
    - There are two types of caves:
        - Big caves (uppercase names): can be visited any number of times.
        - Small caves (lowercase names): can be visited at most once per path.
    - The task is to count all possible distinct paths from the "start" cave to the "end" cave,
      following these visitation rules.

    Args:
        graph (Dict[str, List[str]]): Graph adjacency list.
        current (str): Current cave.
        visited (Set[str]): Set of visited small caves.

    Returns:
        int: Number of distinct paths.
    """
    if current == "end":
        return 1
    count = 0
    # Check if a cave is small (lowercase)
    if current.islower():
        visited = visited | {current}
    for neighbor in graph[current]:
        if neighbor not in visited:
            count += dfs_part_one(graph, neighbor, visited)
    return count


def dfs_part_two(graph: Dict[str, List[str]], current: str, visited: Set[str], small_cave_twice: bool) -> int:
    """
    DFS traversal counting all paths from start to end (Part 2 rules).

    Rules:
    - Same cave system as Part 1.
    - The new rule allows visiting one single small cave **twice**, while all others must be visited at most once.
    - Big caves (uppercase names) can still be visited any number of times.
    - The "start" and "end" caves can only be visited once, no exceptions.
    - The task is to count all distinct paths from "start" to "end" under these rules.

    Args:
        graph (Dict[str, List[str]]): Graph adjacency list.
        current (str): Current cave.
        visited (Set[str]): Set of visited small caves.
        small_cave_twice (bool): Whether a small cave has been visited twice.

    Returns:
        int: Number of distinct paths.
    """
    if current == "end":
        return 1
    count = 0
    # Check if a cave is small (lowercase)
    if current.islower():
        visited = visited | {current}
    for neighbor in graph[current]:
        if neighbor == "start":
            continue
        if neighbor not in visited:
            count += dfs_part_two(graph, neighbor, visited, small_cave_twice)
        elif not small_cave_twice and neighbor in visited:
            count += dfs_part_two(graph, neighbor, visited, True)
    return count


if __name__ == "__main__":
    input_data = get_input("inputs/12_input.txt")

    print(f"Part 1: {dfs_part_one(input_data, 'start', set())}")
    print(f"Part 2: {dfs_part_two(input_data, 'start', set(), False)}")
