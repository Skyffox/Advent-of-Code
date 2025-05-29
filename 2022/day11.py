# pylint: disable=line-too-long
"""
Day 11: Monkey in the Middle

Part 1: What is the level of monkey business after 20 rounds of stuff-slinging simian shenanigans?
Answer: 110885

Part 2: What is the level of monkey business after 10000 rounds?
Answer: 25272176808
"""

from typing import Tuple, List, Dict, Any
from copy import deepcopy
from utils import profiler

Monkey = Dict[str, Any]  # For better clarity, you could use TypedDict or dataclass for stricter typing


def get_input(file_path: str) -> Tuple[List[Monkey], int]:
    """
    Parses the input data to initialize the monkey simulation.

    This function processes the input file, where each monkey's details are provided in 7 lines, 
    with the information parsed and stored in a structured format. The Least Common Multiple (LCM) 
    of the divisibility tests for all monkeys is also computed, which is essential for handling large 
    numbers in Part 2 of the simulation.

    Args:
        file_path (str): The path to the input file containing the monkeys' data.

    Returns:
        Tuple[List[Dict[str, int]], int]: A tuple containing:
            - A list of dictionaries representing each monkey's details, including their items, 
              operation, test value, and outcomes.
            - An integer representing the Least Common Multiple (LCM) of all divisibility tests.
    """
    monkeys = []
    lcm = 1

    with open(file_path, "r", encoding="utf-8") as f:
        input_data = f.readlines()

    for i in range(0, len(input_data), 7):
        items = list(map(int, input_data[i + 1].strip().split(":")[1].strip().split(", ")))
        operation = input_data[i + 2].strip().split(":")[1].strip().split(" = ")[1]
        test = int(input_data[i + 3].strip().split("by")[1].strip())
        if_true = int(input_data[i + 4].strip().split("monkey")[1].strip())
        if_false = int(input_data[i + 5].strip().split("monkey")[1].strip())
        lcm *= test

        monkeys.append({
            'items': items,
            'operation': operation,
            'test': test,
            'if_true': if_true,
            'if_false': if_false,
            'inspections': 0
        })

    return monkeys, lcm


def evaluate_operation(old: int, operation: str) -> int:
    """
    Evaluates and applies the operation on an item, modifying its value based on the operation provided.

    The operation can be either a multiplication or addition, and it is applied to the current item 
    (referred to as `old`). The function supports the specific operation formats described in the problem 
    (e.g., "old * old" or "old * <value>", "old + <value>").

    Args:
        old (int): The current value of the item before the operation is applied.
        operation (str): The operation to be applied, in the format of either multiplication or addition.

    Returns:
        int: The new value of the item after the operation is applied.
    """
    if operation == "old * old":
        return old * old
    elif "*" in operation:
        _, op = operation.split(" * ")
        return old * int(op)
    elif "+" in operation:
        _, op = operation.split(" + ")
        return old + int(op)


@profiler
def simulate_monkey_business(monkeys: List[Monkey], lcm: int, rounds: int = 20, divide: bool = True) -> int:
    """
    Simulates the process of each monkey inspecting and passing items for a given number of rounds.

    Each round consists of every monkey inspecting all their items, performing an operation on each item, 
    testing the result, and passing the item to another monkey based on the test outcome. The `divide` parameter 
    controls whether the item value is divided by 3 after each operation. For Part 2, the worry level is handled 
    using the Least Common Multiple (LCM) of all divisibility tests.

    Args:
        monkeys (List[Dict[str, int]]): A list of dictionaries representing each monkey's details, including their items, 
                                        operation, and test conditions.
        lcm (int): The Least Common Multiple of all divisibility tests, used in Part 2 to handle large numbers.
        rounds (int, optional): The number of rounds to simulate. Defaults to 20 (for Part 1).
        divide (bool, optional): Whether to divide the item value by 3 after each operation. Defaults to True 
                                  (for Part 1). Set to False for Part 2 to avoid division.

    Returns:
        int: The final level of monkey business, calculated as the product of the highest two inspection counts.
    """
    for _ in range(rounds):
        for monkey in monkeys:
            while monkey['items']:
                item = monkey['items'].pop(0)
                monkey['inspections'] += 1

                # Apply the operation to the item
                item = evaluate_operation(item, monkey['operation'])

                # For Part 1, the item is divided by 3
                if divide:
                    item //= 3

                # Modulo the item by the LCM to manage large numbers in Part 2
                item %= lcm

                # Test the item and pass it to the appropriate monkey
                if item % monkey['test'] == 0:
                    monkeys[monkey['if_true']]['items'].append(item)
                else:
                    monkeys[monkey['if_false']]['items'].append(item)

    # Sort inspection counts in descending order and return the product of the top two
    inspection_counts = sorted([monkey['inspections'] for monkey in monkeys], reverse=True)
    return inspection_counts[0] * inspection_counts[1]


if __name__ == "__main__":
    monkeys_input, lcm_input = get_input("inputs/11_input.txt")
    monkeys_input_part_2 = deepcopy(monkeys_input)

    # Simulate the monkey business, for a standard of 20 rounds.
    print(f"Part 1: {simulate_monkey_business(monkeys_input, lcm_input)}")

    # Simulate for 10000 rounds and the worry level is not divided by 3 every round. In order to handle the large numbers
    # I modulo the worry level by the least common multiple (LCM) of the divisibility tests for all monkeys.
    print(f"Part 2: {simulate_monkey_business(monkeys_input_part_2, lcm_input, 10000, False)}")
