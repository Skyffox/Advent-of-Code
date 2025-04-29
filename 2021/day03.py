# pylint: disable=line-too-long
"""
Part 1: Calculate a real number from the most common/uncommon bits that form a binary number
Answer: 852500

Part 2: What is the similarity score between the two lists?
Answer: 1007985
"""

from utils import profiler


def most_common_bit(lst: list, idx: int) -> int:
    """Compare the bits for each position and count which bit (0 or 1) is more common"""
    transposed = list(map(list, zip(*lst)))
    return transposed[idx].count(1) >= transposed[idx].count(0)


def get_input(file_path: str) -> list:
    """Get the input data"""
    with open(file_path, "r", encoding="utf-8") as file:
        return [list(map(int, list(line.strip()))) for line in file]


@profiler
def part_1(lst: list) -> int:
    """Calculate the power consumtpion based on binary numbers in our input"""
    gamma_rate, epsilon_rate = 0, 0

    # The gamma rate is the number that is most common in each position the epsilon rate the one that is most uncommon
    # so we transpose the original list so we can easily compare for each position
    transposed = list(map(list, zip(*lst)))
    binary_lst = [bit.count(1) > bit.count(0) for bit in transposed]

    # Convert the rates, which was in binary, to a real number. For each 1 we find we add to the gamma rate
    # For the epsilon rate the zeroes are actually ones (since those are the most uncommon in that case)
    for idx, binary in enumerate(binary_lst[::-1]):
        if binary == 1:
            gamma_rate += 2**idx
        else:
            epsilon_rate += 2**idx

    return gamma_rate * epsilon_rate


@profiler
def part_2(lst: list) -> int:
    """
    Consider all inputs and find the most common/uncommon bit (common for oxygen and uncommon for co2)
    Filter on all inputs that have this bit and repeat this process but only with the inputs that were filtered.
    """
    oxygen_generator, co2_scrubber = lst[::], lst[::]
    i = 0
    while len(oxygen_generator) != 1:
        bit = most_common_bit(oxygen_generator, i)
        oxygen_generator = [l for l in oxygen_generator if l[i] == bit]
        i += 1

    i = 0
    while len(co2_scrubber) != 1:
        bit = most_common_bit(co2_scrubber, i)
        co2_scrubber = [l for l in co2_scrubber if l[i] != bit]
        i += 1

    # Now create a normal number
    oxygen_real = sum([2**idx if b == 1 else 0 for idx, b in enumerate(oxygen_generator[0][::-1])])
    co2_real = sum([2**idx if b == 1 else 0 for idx, b in enumerate(co2_scrubber[0][::-1])])

    return oxygen_real * co2_real


if __name__ == "__main__":
    input_data = get_input("inputs/3_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
