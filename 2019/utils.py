
# pylint: disable=line-too-long
"""
Useful functions to help with puzzles
"""

from collections import defaultdict
from functools import wraps
import time
from typing import List, Optional


def profiler(func):
    """
    A decorator to measure and log the execution time of a function.
    
    This decorator wraps the provided function and tracks the time it takes 
    to execute. The measured execution time is printed to the console 
    with a timestamp.

    Args:
        func (function): The function whose execution time needs to be measured.

    Returns:
        function: A wrapped version of the input function, which logs the execution time.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time() # Record the start time of the function call
        result = func(*args, **kwargs) # Execute the original function
        elapsed_time = time.time() - start_time # Compute the elapsed time
        print(f"Execution time of '{func.__name__}': {elapsed_time:.4f} seconds")
        return result

    return wrapper


class IntcodeComputer:
    """
    Simulates an Intcode virtual machine capable of executing a list of integer instructions.

    The Intcode computer supports position, immediate, and relative parameter modes.
    It is used across many Advent of Code 2019 challenges to interpret a variety of
    custom assembly-like programs.
    """
    def __init__(self, program: List[int], inputs: List[int] = None):
        """
        Initializes the IntcodeComputer with a given program and optional input list.

        Args:
            program (List[int]): The initial program code to load into memory.
            inputs (List[int], optional): A list of input values to be used by the program.
        """
        self.memory = defaultdict(int, enumerate(program)) # Supports arbitrary program size
        self.inputs = inputs or []
        self.outputs = []
        self.ptr = 0 # instruction pointer
        self.relative_base = 0
        self.halted = False
        self.paused = False

    def add_input(self, value: int) -> None:
        """
        Adds an input value to the input queue.

        Args:
            value (int): The input value to append.
        """
        self.inputs.append(value)
        self.paused = False

    def get_output(self) -> Optional[int]:
        """
        Retrieves and removes the next available output from the output queue.

        Returns:
            Optional[int]: The next output value, or None if no output is available.
        """
        if self.outputs:
            return self.outputs.pop(0)
        return None

    def get_param(self, mode: int, offset: int) -> int:
        """
        Retrieves a parameter value based on its addressing mode.

        Args:
            mode (int): The parameter mode (0 = position, 1 = immediate, 2 = relative).
            offset (int): Offset from the instruction pointer.

        Returns:
            int: The resolved parameter value.

        Raises:
            Exception: If an unknown parameter mode is encountered.
        """
        if mode == 0: # position mode
            return self.memory[self.memory[self.ptr + offset]]
        elif mode == 1: # immediate mode
            return self.memory[self.ptr + offset]
        elif mode == 2: # relative mode
            return self.memory[self.relative_base + self.memory[self.ptr + offset]]
        else:
            raise Exception(f"Unknown parameter mode: {mode}")

    def set_param(self, mode: int, offset: int, value: int):
        """
        Sets a value in memory based on parameter mode.

        Args:
            mode (int): The parameter mode (0 = position, 2 = relative).
            offset (int): Offset from the instruction pointer.
            value (int): The value to write to memory.

        Raises:
            Exception: If an invalid write mode is encountered.
        """
        if mode == 0:
            self.memory[self.memory[self.ptr + offset]] = value
        elif mode == 2:
            self.memory[self.relative_base + self.memory[self.ptr + offset]] = value
        else:
            raise Exception(f"Invalid write mode: {mode}")

    def run(self):
        """
        Executes the Intcode program starting at the current instruction pointer.

        Execution continues until:
        - The program halts (opcode 99),
        - An output is produced (opcode 4), or
        - Input is required but not available (opcode 3).

        Returns:
            Optional[int]: The next output value if generated; otherwise, None.
        """
        while not self.halted:
            instr = self.memory[self.ptr]
            opcode = instr % 100
            modes = [(instr // 10 ** i) % 10 for i in range(2, 5)]

            if opcode in (1, 2, 7, 8):
                a = self.get_param(modes[0], 1)
                b = self.get_param(modes[1], 2)
                if opcode == 1: # add
                    self.set_param(modes[2], 3, a + b)
                elif opcode == 2: # multiply
                    self.set_param(modes[2], 3, a * b)
                elif opcode == 7: # less than
                    self.set_param(modes[2], 3, int(a < b))
                elif opcode == 8: # equals
                    self.set_param(modes[2], 3, int(a == b))
                self.ptr += 4
            elif opcode == 3: # input
                if not self.inputs:
                    # wait for input
                    self.paused = True
                    return None
                self.set_param(modes[0], 1, self.inputs.pop(0))
                self.ptr += 2
            elif opcode == 4: # output
                val = self.get_param(modes[0], 1)
                self.outputs.append(val)
                self.ptr += 2
                return val
            elif opcode == 5: # jump if true
                self.ptr = self.get_param(modes[1], 2) if self.get_param(modes[0], 1) != 0 else self.ptr + 3
            elif opcode == 6: # jump if false
                self.ptr = self.get_param(modes[1], 2) if self.get_param(modes[0], 1) == 0 else self.ptr + 3
            elif opcode == 9: # adjust relative base
                self.relative_base += self.get_param(modes[0], 1)
                self.ptr += 2
            elif opcode == 99: # halt
                self.halted = True
                return None
            else:
                raise Exception(f"Unknown opcode: {opcode}")

    def copy(self) -> 'IntcodeComputer':
        """
        Creates a deep copy of the current state of the IntcodeComputer.

        Useful for saving state or exploring multiple paths in problems
        involving branching logic.

        Returns:
            IntcodeComputer: A new instance with the same memory and state.
        """
        new_computer = IntcodeComputer([])
        new_computer.memory = self.memory.copy()
        new_computer.ptr = self.ptr
        new_computer.relative_base = self.relative_base
        new_computer.inputs = self.inputs.copy()
        new_computer.outputs = self.outputs.copy()
        new_computer.halted = self.halted
        new_computer.paused = self.paused
        return new_computer
