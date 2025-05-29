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


def get_input(file_path: str) -> Tuple[List[str], List[int], List[List[int]]]:
    """
    Reads the input file and returns the rules, your ticket, and nearby tickets.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        Tuple containing:
            - rules (List[str]): List of rule strings.
            - your_ticket (List[int]): Your ticket values.
            - nearby_tickets (List[List[int]]): Nearby tickets values.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read().strip().split("\n\n")
        rules = content[0].split("\n")
        your_ticket = list(map(int, content[1].split("\n")[1].split(",")))
        nearby_tickets = [list(map(int, line.split(","))) for line in content[2].split("\n")[1:]]
        return rules, your_ticket, nearby_tickets


def parse_rules(rules: List[str]) -> Dict[str, List[Tuple[int, int]]]:
    """
    Parses the rules into a dictionary mapping rule name to valid ranges.

    Args:
        rules (List[str]): List of rule strings.

    Returns:
        Dict[str, List[Tuple[int, int]]]: Mapping from rule names to their valid ranges.
    """
    pattern = re.compile(r"(.+): (\d+)-(\d+) or (\d+)-(\d+)")
    parsed_rules = {}
    for rule in rules:
        match = pattern.match(rule)
        if match:
            name = match.group(1)
            ranges = [(int(match.group(2)), int(match.group(3))), (int(match.group(4)), int(match.group(5)))]
            parsed_rules[name] = ranges
    return parsed_rules


def is_value_valid(value: int, rules: Dict[str, List[Tuple[int, int]]]) -> bool:
    """
    Checks if a value is valid for at least one rule.

    Args:
        value (int): The value to check.
        rules (Dict[str, List[Tuple[int, int]]]): The parsed rules.

    Returns:
        bool: True if valid, False otherwise.
    """
    for ranges in rules.values():
        for low, high in ranges:
            if low <= value <= high:
                return True
    return False


@profiler
def part_one(data_input: Tuple[List[str], List[int], List[List[int]]]) -> int:
    """
    Solves part one: sum of invalid values on nearby tickets.

    Args:
        data_input: Tuple containing rules, your ticket, and nearby tickets.

    Returns:
        int: Sum of all invalid values.
    """
    rules, _, nearby_tickets = data_input
    parsed_rules = parse_rules(rules)
    invalid_sum = 0
    for ticket in nearby_tickets:
        for value in ticket:
            if not is_value_valid(value, parsed_rules):
                invalid_sum += value
    return invalid_sum


def is_ticket_valid(ticket: List[int], rules: Dict[str, List[Tuple[int, int]]]) -> bool:
    """
    Checks if a ticket is valid by checking all values against the rules.

    Args:
        ticket (List[int]): The ticket to check.
        rules (Dict[str, List[Tuple[int, int]]]): The parsed rules.

    Returns:
        bool: True if valid, False otherwise.
    """
    return all(is_value_valid(value, rules) for value in ticket)


def determine_field_order(valid_tickets: List[List[int]], rules: Dict[str, List[Tuple[int, int]]]) -> List[str]:
    """
    Determines the field order based on valid tickets and rules.

    Args:
        valid_tickets (List[List[int]]): List of valid tickets.
        rules (Dict[str, List[Tuple[int, int]]]): Parsed rules.

    Returns:
        List[str]: Ordered list of field names.
    """
    field_possibilities = {i: set(rules.keys()) for i in range(len(valid_tickets[0]))}

    for ticket in valid_tickets:
        for i, value in enumerate(ticket):
            invalid_fields = set()
            for field in field_possibilities[i]:
                ranges = rules[field]
                if not any(low <= value <= high for low, high in ranges):
                    invalid_fields.add(field)
            field_possibilities[i] -= invalid_fields

    determined_fields = {}
    while field_possibilities:
        # Find fields with only one possibility
        resolved = {pos: next(iter(fields)) for pos, fields in field_possibilities.items() if len(fields) == 1}
        for pos, field in resolved.items():
            determined_fields[pos] = field
            del field_possibilities[pos]
            for fields in field_possibilities.values():
                fields.discard(field)

    # Order fields by position
    return [determined_fields[i] for i in range(len(determined_fields))]


@profiler
def part_two(data_input: Tuple[List[str], List[int], List[List[int]]]) -> int:
    """
    Solves part two: product of 'departure' fields on your ticket.

    Args:
        data_input: Tuple containing rules, your ticket, and nearby tickets.

    Returns:
        int: Product of all 'departure' fields on your ticket.
    """
    rules, your_ticket, nearby_tickets = data_input
    parsed_rules = parse_rules(rules)
    valid_tickets = [ticket for ticket in nearby_tickets if is_ticket_valid(ticket, parsed_rules)]
    valid_tickets.append(your_ticket)  # include your ticket

    field_order = determine_field_order(valid_tickets, parsed_rules)

    product = 1
    for i, field in enumerate(field_order):
        if field.startswith("departure"):
            product *= your_ticket[i]
    return product


if __name__ == "__main__":
    input_data = get_input("inputs/16_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
