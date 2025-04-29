# pylint: disable=line-too-long
"""
Part 1: What is the level of monkey business after 20 rounds of stuff-slinging simian shenanigans?
Answer: 110885

Part 2: What is the level of monkey business after 10000 rounds?
Answer: 25272176808
"""

from copy import deepcopy
from utils import profiler


def get_input(file_path: str) -> tuple[list, int]:
    """
    Parse the input data, first get all the input data then proces every 7 lines as that describes one monkey.
    The Least Common Multiple of each monkeys divisor in our case is simply the product, since they're all primes.
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


def evaluate_operation(old, operation):
    """a"""
    # Evaluates the operation on the current item
    if operation == "old * old":
        return old * old
    elif "*" in operation:
        _, op = operation.split(" * ")
        return old * int(op)
    elif "+" in operation:
        _, op = operation.split(" + ")
        return old + int(op)


def simulate_monkey_business(monkeys, lcm, rounds=20, divide=True):
    """a"""
    for _ in range(rounds):
        for monkey in monkeys:
            while monkey['items']:
                item = monkey['items'].pop(0)
                monkey['inspections'] += 1

                # Perform the operation on the item
                item = evaluate_operation(item, monkey['operation'])

                # after each operation, the worry level (the value of the item) is divided by 3 before being passed to another monkey.
                if divide:
                    item //= 3

                item %= lcm

                # Test the item
                if item % monkey['test'] == 0:
                    monkeys[monkey['if_true']]['items'].append(item)
                else:
                    monkeys[monkey['if_false']]['items'].append(item)

    # Get the number of inspections by all monkeys, sorted in descending order
    inspection_counts = sorted([monkey['inspections'] for monkey in monkeys], reverse=True)
    return inspection_counts[0] * inspection_counts[1]


if __name__ == "__main__":
    # Parse the input
    monkeys_input, lcm_input = get_input("inputs/11_input.txt")
    monkeys_input_part_2 = deepcopy(monkeys_input)

    # Simulate the monkey business, for a standard of 20 rounds.
    print(simulate_monkey_business(monkeys_input, lcm_input))

    # Simulate for 10000 rounds and the worry level is not divided by 3 every round. In order to handle the large numbers 
    # I modulo the worry level by the least common multiple (LCM) of the divisibility tests for all monkeys.
    print(simulate_monkey_business(monkeys_input_part_2, lcm_input, 10000, False))



# Explanation of the Solution:
# parse_monkey_input: This function takes the input data and parses the monkey's information into a list of dictionaries. Each dictionary contains the items the monkey starts with, the operation they perform, the divisibility test, and where to send the items based on the test result.

# evaluate_operation: This function handles the operation that each monkey performs on the items. The operation can either be a multiplication or addition, and it works on the current item (old).

# simulate_monkey_business: This function simulates the process of each monkey inspecting and passing items. For each round, each monkey inspects all of their items, performs the operation, and tests the result to pass it to the appropriate monkey.

# calculate_monkey_business: After simulating the rounds, we calculate the "monkey business" by sorting the number of inspections each monkey made and multiplying the top two values.



# Problem 11: Monkey in the Middle
# Problem Overview:
# You are tasked with simulating a set of monkeys passing around items, performing operations on them, and testing divisibility. Each monkey starts with a certain set of items, and for each item:

# The monkey performs a mathematical operation.
# The result is tested to see if it is divisible by a certain number.
# Depending on the result of the test, the item is passed to another monkey.
# The goal is to simulate the process and calculate the "monkey business," which is the product of the two monkeys that inspected the most items.

# Approach:
# The problem is a simulation involving the following steps:

# Initial Setup: Each monkey starts with a list of items.
# Operations: Each monkey performs a specified operation on the items they are holding (like multiplying by a constant, adding a constant, etc.).
# Divisibility Test: Each monkey tests whether the item value is divisible by a given number.
# Passing Items: If an item passes the test, it goes to one monkey; otherwise, it goes to another.
# Counting Inspections: Each monkey keeps track of how many items they inspect during the process.
# Calculating the Result: The "monkey business" is calculated by multiplying the two monkeys that inspected the most items.


