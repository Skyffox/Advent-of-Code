# pylint: disable=line-too-long
"""
Day 8: Haunted Wasteland

Part 1: How many steps does it take node 'AAA' to reach node 'ZZZ'?
Answer: 19241

Part 2: Find the amount of steps it takes for every input that ends in 'A' to end up in a node that ends in 'Z'.
Answer: 9606140307013
"""

from functools import reduce
from typing import List, Dict, Tuple
from utils import profiler


def get_input(file_path: str) -> Tuple[List[str], Dict[str, Tuple[str, str]]]:
    """
    Reads the input from a file and parses it into a list of directions and a dictionary of nodes.
    The directions indicate whether to move left ('L') or right ('R') at each step. Each node
    in the network has two possible directions leading to different neighboring nodes. 

    Args:
        file_path (str): The path to the input file.

    Returns:
        Tuple[List[str], Dict[str, Tuple[str, str]]]: 
            A tuple where:
                - The first element is a list of directions ('L' and 'R').
                - The second element is a dictionary where each key is a node ID (string), 
                  and the value is a tuple of two strings representing the possible 
                  neighboring nodes for that node.
    """
    nodes = {}
    inp = []
    with open(file_path, "r", encoding="utf-8") as file:
        for i, line in enumerate(file):
            line = line.strip()
            if i == 0:
                inp = list(line) # The list of directions ('L' and 'R')
            elif line:
                key, value = line.split(" = ")
                # Split the paths into two strings, one for each direction.
                paths = [x for x in value if x.isalpha()]
                nodes[key] = ("".join(paths[:3]), "".join(paths[3:]))
    return inp, nodes


def gcd(x: int, y: int) -> int:
    """
    Computes the Greatest Common Divisor (GCD) of two integers using the Euclidean algorithm.
    The GCD of two numbers is the largest integer that divides both of them without leaving a remainder.

    Args:
        x (int): The first integer.
        y (int): The second integer.

    Returns:
        int: The greatest common divisor of `x` and `y`.
    """
    while y:
        x, y = y, x % y
    return x


def lcm(x: int, y: int) -> int:
    """
    Computes the Least Common Multiple (LCM) of two integers.
    The LCM of two numbers is the smallest number that is a multiple of both numbers.
    It can be calculated by multiplying the two numbers and dividing by their GCD.

    Args:
        x (int): The first integer.
        y (int): The second integer.

    Returns:
        int: The least common multiple of `x` and `y`.
    """
    return (x * y) // gcd(x, y)


def find_end(curr_pos: str, nodes: Dict[str, Tuple[str, str]], inp: List[str]) -> int:
    """
    Simulates moving through the nodes according to the given list of directions until reaching 
    a node that ends with 'Z'. It counts the number of steps required to reach such a node.

    Starting from `curr_pos`, the function repeatedly follows the directions ('L' for left, 'R' for right)
    from the current node until a node that ends with 'Z' is reached.

    Args:
        curr_pos (str): The starting position, represented as a node ID.
        nodes (Dict[str, Tuple[str, str]]): A dictionary where each node ID maps to a tuple of two neighboring nodes.
        inp (List[str]): A list of directions ('L' or 'R') to follow at each step.

    Returns:
        int: The number of steps it takes to reach a node that ends with 'Z'.
    """
    counter = 0
    while True:
        for direction in inp:
            # Move to the next node depending on the direction.
            curr_pos = nodes[curr_pos][0] if direction == 'L' else nodes[curr_pos][1]
            counter += 1
            # Check if the last character of the current position is 'Z'.
            if curr_pos[-1] == 'Z':
                return counter


@profiler
def part_1(nodes: Dict[str, Tuple[str, str]], inp: List[str]) -> int:
    """
    Calculates the number of steps it takes to go from node 'AAA' to node 'ZZZ' following the 
    provided list of directions at each step.

    This function calls `find_end` to simulate the movement through the nodes and returns the 
    number of steps required to reach a node that ends with 'Z'.

    Args:
        nodes (Dict[str, Tuple[str, str]]): A dictionary where each node ID maps to a tuple of two neighboring nodes.
        inp (List[str]): A list of directions ('L' or 'R') to follow at each step.

    Returns:
        int: The number of steps it takes to reach a node ending in 'Z', starting from node 'AAA'.
    """
    return find_end('AAA', nodes, inp)


@profiler
def part_2(nodes: Dict[str, Tuple[str, str]], inp: List[str]) -> int:
    """
    Simultaneously computes the number of steps for every node that ends with 'A' to reach a node 
    that ends with 'Z', then computes the Least Common Multiple (LCM) of all those step counts.

    This function collects all nodes that end with 'A', then finds how many steps it takes for 
    each to reach a node ending in 'Z'. It then calculates the LCM of the resulting step counts.

    Args:
        nodes (Dict[str, Tuple[str, str]]): A dictionary where each node ID maps to a tuple of two neighboring nodes.
        inp (List[str]): A list of directions ('L' or 'R') to follow at each step.

    Returns:
        int: The Least Common Multiple (LCM) of the steps it takes for each node ending in 'A' to reach a node ending in 'Z'.
    """
    starting_pos = [node for node in nodes if node[-1] == 'A']
    ending_pos = [find_end(pos, nodes, inp) for pos in starting_pos]
    
    # Compute the LCM of all the ending positions (steps).
    return reduce(lcm, ending_pos)


if __name__ == "__main__":
    input_start, node_dict = get_input("inputs/8_input.txt")

    print(f"Part 1: {part_1(node_dict, input_start)}")
    print(f"Part 2: {part_2(node_dict, input_start)}")
