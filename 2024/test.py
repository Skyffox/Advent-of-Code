# pylint: disable=line-too-long
"""
Test suite for the AoC solutions for 2024 (for now). 
Since all our modules contain the standard entry point of if __name__ == "__main__" we can not simply run 
the module to get our output. We also can not run the individual functions because they require variable arguments.
So instead I will use the subprocess.run() function to read the stdout of each file in this directory and 
compare that with the answers given by the AoC website.
"""

import subprocess
import time
import os
import fnmatch
import re


def find_file(pattern, path):
    """Walk the directory for the 'path' variable and return the file that matches the pattern"""
    for _, _, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                return name


def run_tests() -> None:
    """Run all AoC 2024 days and compare the output against the answers"""
    total_time: float = 0.0 # In seconds
    num_pass: int = 0
    num_fail: int = 0
    num_remain: int = len(ANSWERS)

    for (prob, expect_answers) in sorted(ANSWERS.items()):
        start_time: float = time.time()

        # Find file in the current directory that has the following format: dayXX.py
        module = find_file(f'day{prob:02}.py', os.getcwd())

        # Run the entire file as a subprocces and pipe the output to stdout
        output: str = subprocess.run(f'python3 {module}', check=False, capture_output=True, text=True).stdout

        # Answer are always in the form: Part X: XXXXX
        output = re.findall(r'Part .:.+\n', output)

        answer_part_1 = output[0].split(":")[1].strip()
        answer_part_2 = output[1].split(":")[1].strip()

        elapsed_time: float = time.time() - start_time
        total_time += elapsed_time

        if answer_part_1 == expect_answers[0] and answer_part_2 == expect_answers[1]:
            failstr: str = ""
            num_pass += 1
        else:
            failstr = "    *** FAIL ***"
            num_fail += 1

        num_remain -= 1

        print(f"\r{' '*70}\r", end="")
        print(f"Problem {prob:03}: {int(round(elapsed_time * 1000)):7} ms{failstr}")

    print(f"Elapsed = {int(total_time)} s, Passed = {num_pass}, Failed = {num_fail}, Remaining = {num_remain}", end="", flush=True)


ANSWERS: dict[int, list] = {
	  1 : ["2031679", "19678534"],
	  2 : ["407", "459"],
	  3 : ["184511516", "90044227"],
	  4 : ["2532", "1941"],
	  5 : ["6498", "5017"],
	  6 : ["5030", "1928"],
	  7 : ["975671981569", "223472064194845"],
	  8 : ["301", "1019"],
	  9 : ["6435922584968", "6469636832766"],
	 10 : ["796", "1942"],
     11 : ["172484", "205913561055242"],
     12 : ["1400386", "851994"],
     13 : ["38714", "74015623345775"],
     14 : ["216027840", "6876"],
     15 : ["1479679", "1509780"]
}


if __name__ == "__main__":
    run_tests()
