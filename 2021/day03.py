# Part 1: Calculate a real number from the most common/uncommon bits that form a binary number
# Answer: 852500

# Part 2: 
# Answer: 1007985


def most_common_bit(lst, idx):
    transposed = list(map(list, zip(*lst)))
    return 1 if transposed[idx].count(1) >= transposed[idx].count(0) else 0


lst, binary_lst = [], []
gamma_rate, epsilon_rate = 0, 0
with open("inputs/3_input.txt") as f:
    for line in f:
        lst.append(list(map(int, list(line.strip()))))

    # Part 1
    # The gamma rate is the number that is most common in each position the epsilon rate the one that is most uncommon
    # so we transpose the original list so we can easily compare for each position
    transposed = list(map(list, zip(*lst)))
    binary_lst = [1 if bit.count(1) > bit.count(0) else 0 for bit in transposed]

    # Convert the rates, which was in binary, to a real number. For each 1 we find we add to the gamma rate
    # For the epsilon rate the zeroes are actually ones (since those are the most uncommon in that case)
    for idx, binary in enumerate(binary_lst[::-1]):
        if binary == 1: 
            gamma_rate += 2**idx
        else:
            epsilon_rate += 2**idx

    # Part 2
    # So its a bit complicated what we are going to do, but... We are going to find the most common bit in 
    # each position and then drop lists which do not have the most common bit in that position
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


print("Part 1", gamma_rate * epsilon_rate)
print("Part 1", oxygen_real * co2_real)