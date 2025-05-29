# pylint: disable=line-too-long
"""
Day 12: Digital Plumber

Part 1: How many programs are in the group that contains program ID 0?
Answer: 152

Part 2: How many groups are there in total?
Answer: 186
"""

from typing import List, Dict, Set
from utils import profiler


def get_input(file_path: str) -> Dict[int, List[int]]:
    """
    Reads the input file and returns a list of connection lines.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        Dict[int, List[int]]: Graph adjacency list.
    """
    graph = {}
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            node_str, neighbors_str = line.split(" <-> ")
            node = int(node_str)
            neighbors = list(map(int, neighbors_str.split(", ")))
            graph[node] = neighbors

    return graph


def dfs(graph: Dict[int, List[int]], start: int, visited: Set[int]) -> None:
    """
    Depth-first search to mark all connected nodes.

    Args:
        graph (Dict[int, List[int]]): Graph adjacency list.
        start (int): Starting node.
        visited (Set[int]): Set of visited nodes.
    """
    stack = [start]
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            stack.extend(graph[node])


@profiler
def part_one(graph: List[str]) -> int:
    """
    Counts number of nodes in the group containing node 0.

    Args:
        data_input (List[str]): Input connection lines.

    Returns:
        int: Size of group containing node 0.
    """
    visited = set()
    dfs(graph, 0, visited)
    return len(visited)


@profiler
def part_two(graph: List[str]) -> int:
    """
    Counts number of distinct groups in the graph.

    Args:
        data_input (List[str]): Input connection lines.

    Returns:
        int: Number of groups.
    """
    visited = set()
    groups = 0

    for node in graph.keys():
        if node not in visited:
            dfs(graph, node, visited)
            groups += 1

    return groups


if __name__ == "__main__":
    input_data = get_input("inputs/12_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
