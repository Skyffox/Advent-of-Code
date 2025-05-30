# pylint: disable=line-too-long
"""
Day 16: Ticket Translation

Part 1: Consider the validity of the nearby tickets you scanned. What is your ticket scanning error rate?
Answer: 19087

Part 2: Once you work out which field is which, look for the six fields on your ticket that start with the word departure. 
        What do you get if you multiply those six values together?
Answer: 1382443095281
"""

import re
from typing import List, Tuple, Dict
from utils import profiler


def load_and_parse_input(file_path: str) -> Tuple[Dict[str, List[Tuple[int, int]]], List[int], List[List[int]]]:
    """
    Reads and parses the input file into rules, your ticket, and nearby tickets.

    Args:
        file_path (str): Path to the input file.

    Returns:
        Tuple containing:
            - rules (Dict[str, List[Tuple[int, int]]]): 
                Mapping from field names to their valid value ranges.
            - your_ticket (List[int]): The list of integers on your ticket.
            - nearby_tickets (List[List[int]]): List of nearby tickets, each a list of integers.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read().strip().split("\n\n")

    # Compile regex pattern to parse each rule line
    rule_pattern = re.compile(r"(.+): (\d+)-(\d+) or (\d+)-(\d+)")
    rules = {}

    # Parse each rule line into dictionary entries
    for line in content[0].split("\n"):
        match = rule_pattern.match(line)
        if match:
            field_name = match.group(1)
            ranges = [
                (int(match.group(2)), int(match.group(3))),
                (int(match.group(4)), int(match.group(5)))
            ]
            rules[field_name] = ranges

    # Parse your ticket values from the second section
    your_ticket = list(map(int, content[1].split("\n")[1].split(",")))

    # Parse nearby tickets values from the third section
    nearby_tickets = [list(map(int, line.split(","))) for line in content[2].split("\n")[1:]]

    return rules, your_ticket, nearby_tickets


def is_value_valid(value: int, rules: Dict[str, List[Tuple[int, int]]]) -> bool:
    """
    Checks if a single value satisfies at least one of the valid ranges from any rule.

    Args:
        value (int): The value to validate.
        rules (Dict[str, List[Tuple[int, int]]]): Mapping of rules to their valid ranges.

    Returns:
        bool: True if value is valid for any rule; False otherwise.
    """
    for ranges in rules.values():
        for low, high in ranges:
            if low <= value <= high:
                return True
    return False


@profiler
def part_one(data_input: Tuple[Dict[str, List[Tuple[int, int]]], List[int], List[List[int]]]) -> int:
    """
    Calculates the ticket scanning error rate by summing invalid values
    found on nearby tickets (values that don't satisfy any rule).

    Args:
        data_input (Tuple): Parsed input containing rules, your ticket, and nearby tickets.

    Returns:
        int: Sum of all invalid values found on nearby tickets.
    """
    rules, _, nearby_tickets = data_input
    invalid_sum = 0

    # Iterate over all nearby tickets and their values
    for ticket in nearby_tickets:
        for value in ticket:
            # Accumulate values that don't satisfy any rule
            if not is_value_valid(value, rules):
                invalid_sum += value

    return invalid_sum


def is_ticket_valid(ticket: List[int], rules: Dict[str, List[Tuple[int, int]]]) -> bool:
    """
    Determines if all values in a ticket satisfy at least one rule.

    Args:
        ticket (List[int]): The ticket values.
        rules (Dict[str, List[Tuple[int, int]]]): Mapping of rules to valid ranges.

    Returns:
        bool: True if all values are valid for at least one rule, False otherwise.
    """
    return all(is_value_valid(value, rules) for value in ticket)


def determine_field_order(
    valid_tickets: List[List[int]], rules: Dict[str, List[Tuple[int, int]]]
) -> List[str]:
    """
    Determines the order of fields on the tickets by elimination.

    Args:
        valid_tickets (List[List[int]]): List of tickets that are all valid.
        rules (Dict[str, List[Tuple[int, int]]]): Rules mapping field names to valid ranges.

    Returns:
        List[str]: List of field names ordered by their position index on the tickets.
    """
    # Start assuming each field index can correspond to any rule name
    field_possibilities = {i: set(rules.keys()) for i in range(len(valid_tickets[0]))}

    # Narrow down field possibilities based on ticket values
    for ticket in valid_tickets:
        for idx, value in enumerate(ticket):
            invalid_fields = set()
            for field in field_possibilities[idx]:
                ranges = rules[field]
                # Mark field invalid if value doesn't satisfy any of its ranges
                if not any(low <= value <= high for low, high in ranges):
                    invalid_fields.add(field)
            field_possibilities[idx] -= invalid_fields  # Remove invalid fields for this position

    determined_fields = {}

    # Repeatedly resolve fields with only one possibility and remove them from others
    while field_possibilities:
        resolved = {
            idx: next(iter(fields)) for idx, fields in field_possibilities.items() if len(fields) == 1
        }
        for idx, field in resolved.items():
            determined_fields[idx] = field
            del field_possibilities[idx]
            for fields in field_possibilities.values():
                fields.discard(field)

    # Return fields ordered by their position on the ticket
    return [determined_fields[i] for i in range(len(determined_fields))]


@profiler
def part_two(data_input: Tuple[Dict[str, List[Tuple[int, int]]], List[int], List[List[int]]]) -> int:
    """
    Determines which fields correspond to which positions on the tickets, then
    calculates the product of the values on your ticket for fields starting with 'departure'.

    Args:
        data_input (Tuple): Parsed input containing rules, your ticket, and nearby tickets.

    Returns:
        int: Product of all 'departure' field values on your ticket.
    """
    rules, your_ticket, nearby_tickets = data_input

    # Filter out invalid tickets to only work with fully valid ones
    valid_tickets = [t for t in nearby_tickets if is_ticket_valid(t, rules)]
    valid_tickets.append(your_ticket)  # Include your own ticket for field determination

    # Determine the mapping from field positions to field names
    field_order = determine_field_order(valid_tickets, rules)

    product = 1
    # Multiply the values of all fields whose name starts with "departure"
    for idx, field_name in enumerate(field_order):
        if field_name.startswith("departure"):
            product *= your_ticket[idx]

    return product


if __name__ == "__main__":
    input_data = load_and_parse_input("inputs/16_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
