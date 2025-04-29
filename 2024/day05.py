# pylint: disable=line-too-long
"""
Part 1: See if the given pages from the input are in the right order
Answer: 6498

Part 2: Fix the incorrectly ordered updates by applying the ordering rules
Answer: 5017
"""

from utils import profiler


def get_input(file_path: str) -> tuple[list, list]:
    """Get the input data"""
    pages, rules = [], []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if "|" in line:
                line = line.split("|")
                rules.append((int(line[0]), int(line[1])))
            else:
                if line != "":
                    pages.append(list(map(int, line.split(","))))

    return pages, rules


def check_correctness(page: list, rules: list) -> bool:
    """Apply the rules that came with the input and see if a page is in the correct order"""
    for idx, page_number in enumerate(page):
        for rule in rules:
            # Check the first number of each rule, if the second number in the rule
            # comes before the first number in the page then the order is incorrect
            if rule[0] == page_number and rule[1] in page[:idx]:
                return False
    return True


@profiler
def part_1(pages: list, rules: list) -> int:
    """See how many pages are in the correct order, get the median of each correct page"""
    return sum([page[len(page) // 2] for page in pages if check_correctness(page, rules)])


@profiler
def part_2(pages: list, rules: list) -> int:
    """See if we can fix an incorrect page based on the given rules"""
    n = 0
    for page in pages:
        if not check_correctness(page, rules):
            orders = []
            for page_number2 in page:
                # Get all the rules that are associated with a page number
                orders.append([page_number2, len([rule for rule in ordering_rules if rule[0] == page_number2 and rule[1] in page])]) 

            # Order based on the amount of rules there are for each number, then we know where it will end up in the order
            orders.sort(key=lambda x: x[1], reverse=True)

            # Get the middle element of the now fixed page
            n += orders[len(page)//2][0]
    return n


if __name__ == "__main__":
    # Get input data
    input_data, ordering_rules = get_input("inputs/5_input.txt")

    print(f"Part 1: {part_1(input_data, ordering_rules)}")
    print(f"Part 2: {part_2(input_data, ordering_rules)}")
