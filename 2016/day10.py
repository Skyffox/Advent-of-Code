# pylint: disable=line-too-long
"""
Day 10: Balance Bots

Part 1: Based on your instructions, what is the number of the bot that is responsible for comparing value-61 microchips with value-17 microchips?
Answer: 157

Part 2: What do you get if you multiply together the values of one chip in each of outputs 0, 1, and 2?
Answer: 71184
"""

import re
from typing import List, Dict, Tuple
from utils import profiler


def get_input(file_path: str) -> List[str]:
    """
    Reads the input file and returns a list of instruction lines.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        list[str]: List of instructions.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file]


@profiler
def compute(data_input: List[str]) -> Tuple[int, int]:
    """
    Simulates bots comparing microchips to find the bot that compares chip 61 and 17 and
    after running the simulation, multiplies outputs 0,1,2 chip values.

    Args:
        data_input (List[str]): List of instructions.

    Returns:
        int: The bot number responsible for comparing chips 61 and 17.
        int: Product of chips in outputs 0, 1, and 2.
    """
    bots: Dict[int, List[int]] = {}
    outputs: Dict[int, List[int]] = {}
    instructions = []
    answer_part_1 = -1

    for line in data_input:
        if line.startswith("value"):
            value, bot = map(int, re.findall(r'\d+', line))
            bots.setdefault(bot, []).append(value)
        else:
            instructions.append(line)

    # Run simulation until no bot can act
    while True:
        action_performed = False
        for instr in instructions:
            m = re.match(r'bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)', instr)
            if not m:
                continue
            bot_id = int(m.group(1))
            low_type, low_id = m.group(2), int(m.group(3))
            high_type, high_id = m.group(4), int(m.group(5))

            if bot_id in bots and len(bots[bot_id]) == 2:
                chips = sorted(bots[bot_id])

                # Check for part 1 condition: comparing 61 and 17
                if set(chips) == {17, 61}:
                    answer_part_1 = bot_id

                if low_type == 'bot':
                    bots.setdefault(low_id, []).append(chips[0])
                else:
                    outputs.setdefault(low_id, []).append(chips[0])

                if high_type == 'bot':
                    bots.setdefault(high_id, []).append(chips[1])
                else:
                    outputs.setdefault(high_id, []).append(chips[1])

                bots[bot_id] = []
                action_performed = True
        if not action_performed:
            break

    # Multiply chips in outputs 0, 1, and 2
    return answer_part_1, outputs.get(0, [1])[0] * outputs.get(1, [1])[0] * outputs.get(2, [1])[0]


if __name__ == "__main__":
    input_data = get_input("inputs/10_input.txt")
    specific_bot, multiplied_outputs = compute(input_data)

    print(f"Part 1: {specific_bot}")
    print(f"Part 2: {multiplied_outputs}")
