# pylint: disable=line-too-long
"""
Part 1: Find the signal strength during the 20th, 60th, 100th, 140th, 180th, and 220th cycles. What is the sum of these six signal strengths?
Answer: 13920

Part 2: Render the image given by your program. What eight capital letters appear on your CRT?
Answer: EGLHBLFJ
"""

from utils import profiler


def get_input(file_path: str) -> list:
    """Get the input data"""
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip().split() for line in file]


@profiler
def part_1(lines: list) -> int:
    """Find the signal strength during specific cycles"""
    total, counter, initial_value = 0, 1, 1
    cycles = [20, 60, 100, 140, 180, 220]

    for line in lines:
        for idx, _ in enumerate(line):
            if counter in cycles:
                total += (initial_value * counter)

            counter += 1

            # "addx V" command takes two cycles to complete
            # After two cycles, the X register is increased by the value V
            if idx == 1:
                initial_value += int(line[1])

    return total


@profiler
def part_2(lines: list) -> str:
    """Generate an image"""
    message, row = [], []
    initial_value, counter = 1, 1
    for line in lines:
        for idx, _ in enumerate(line):
            # The CRT is 40 pixels wide
            pos = counter % 40

            # If the sprite is positioned such that one of its three pixels is the
            # pixel currently being drawn, the screen produces a lit pixel
            if pos in range(initial_value, initial_value + 3):
                row.append("# ")
            else:
                row.append(". ")

            if pos == 0:
                message.append(row)
                row = []

            counter += 1

            if idx == 1:
                initial_value += int(line[1])

    # NOTE: The message spells out the following letters: EGLHBLFJ
    # for x in message:
    #     print("".join(x))

    return "EGLHBLFJ"


if __name__ == "__main__":
    input_data = get_input("inputs/10_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
