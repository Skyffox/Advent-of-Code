# pylint: disable=line-too-long
"""
Part 1: Using the information provided by the debugger, initialize the registers to the given values, 
        then run the program. Once it halts, what do you get if you use commas to join the values it output into a single string?
Answer: 7,0,3,1,2,6,3,7,1

Part 2: What is the lowest positive initial value for register A that causes the program to output a copy of itself?
Answer: 109020013201563
"""

from utils import profiler


def get_input(file_path: str) -> list:
    """Get the input data"""
    with open(file_path, "r", encoding="utf-8") as file:
        data = file.readlines()
        a = int(''.join([char for char in data[0] if char.isdigit()]))
        program = list(map(int, [char for char in data[4] if char.isdigit()]))

    return a, program


def part_1(program: list, register_a: int, register_b: int, register_c: int) -> list:
    """
    Follow the instructions from our program, every iteration has an opcode that represents an 
    operation and an operand that may be needed in an operation.
    """
    ptr = 0
    out = []

    def combo(operand):
        if operand == 4:
            return register_a
        if operand == 5:
            return register_b
        if operand == 6:
            return register_c
        return operand

    # Keep running the program until opcode 3 basically doesn't jump us back to the start.
    while ptr < len(program):
        opcode, operand = program[ptr:ptr+2]

        match opcode:
            case 0:
                # Shifting bits to the right by n positions is equivalent to performing integer division by 2**n
                register_a >>= combo(operand)
            case 1:
                # Bitwise XOR on register B and the instructions literal operand
                register_b ^= operand
            case 2:
                register_b = combo(operand) % 8
            case 3:
                # Jumps to the start if the value of register A is not zero
                if register_a != 0:
                    ptr = operand - 2
            case 4:
                register_b ^= register_c
            case 5:
                # Output the instructions literal operand modulo 8
                out.append(combo(operand) % 8)
            case 6:
                register_b = register_a >> combo(operand)
            case 7:
                register_c = register_a >> combo(operand)

        ptr += 2

    return out


@profiler
def part_2(program: list) -> int:
    """
    This was really nasty to figure out, so first I translated my puzzle input into pseudocode on paper. That looked like this:
    B = A % 8
    B = B ^ B
    C = A >> B
    A = A >> 3
    B = B ^ C
    A = A >> C
    OUT B
    if A != 0 JMP 0

    From the pseudocode I noticed a couple of things: the program will only stop if A becomes 0 and since there is only one print 
    command in the program, the whole program has to run 16 times to get the exact same input. And the value of the output is fully
    determined by the value of A.
    
    I also noticed that A is divided by 2**3 (8, or bitshifted 3 times) every loop and basically keeps running until we hit 0. 
    Furthermore, you can see that each iteration begins with 'B = A modulo 8'. If you put that together with the 'A = A // 8' that happens every loop, 
    you can understand this as each loop "using up" the least significant digit of A.

    So now we can work our way backwards through the expected output (the program), starting with an A value of 0, and see which of the 8 potential 
    initial A values actually outputs the expected value.
    """
    register_a = 0
    for i in reversed(range(len(program))):
        register_a *= 8
        while part_1(program, register_a, 0, 0) != program[i:]:
            register_a += 1

    return register_a


if __name__ == "__main__":
    # Get input data
    A_input, program_input = get_input("inputs/17_input.txt")

    print(f"Part 1: {part_1(program_input, A_input, 0, 0)}")
    print(f"Part 2: {part_2(program_input)}")
