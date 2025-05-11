# pylint: disable=line-too-long
"""
Test Suite for Advent of Code Solutions

This script runs tests for the Advent of Code solutions, comparing their outputs against the expected results.
Since each solution module has a standard entry point `if __name__ == "__main__"`, we can't simply run the modules directly or call the functions 
due to their need for variable arguments. Instead, this script uses `subprocess.run()` to execute each module and capture its output, 
which is then compared to the expected output for each problem.
"""

import os
import fnmatch
import re
import subprocess
import time
from typing import Dict, List


def find_file(pattern: str, path: str) -> str:
	"""
	Searches for a file in the given directory that matches the provided pattern.

	This function walks through the specified directory recursively and returns 
	the first file whose name matches the given pattern.

	Args:
		pattern (str): The pattern to match the filenames.
		path (str): The directory path to search for files.

	Returns:
		str: The filename that matches the pattern, or an empty string if no match is found.
	"""
	for _, _, files in os.walk(path):
		for name in files:
			if fnmatch.fnmatch(name, pattern):
				return name
	return ""


def run_tests(year: str, answers: Dict[int, List[str]]) -> None:
    """
    Executes the test suite for all Advent of Code solutions per year and compares the results 
    to the expected answers. The function uses `subprocess.run()` to run each solution 
    and compares the output with pre-defined expected answers.

    The results are displayed in the format:
    - Problem number
    - Execution time in milliseconds
    - Pass/Fail status for each problem

    Finally, it displays the total time taken and the number of tests that passed/failed.
    """
    total_time: float = 0.0 # In seconds
    num_pass: int = 0
    num_fail: int = 0

    print(f"\nTesting problem for year {year}")
    os.chdir(year)

    for prob, expect_answers in sorted(answers.items()):
        start_time: float = time.time()

        # Find file in the current directory that has the following format: dayXX.py
        module = find_file(f'day{prob:02}.py', os.getcwd())

        # Run the solution file as a subprocess and capture the output
        output = subprocess.run(
            f'python3 {module}', check=False, capture_output=True, text=True
        ).stdout

        # Answers are always in the form: Part X: XXXXX
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

        # Print the results for the current problem
        print(f"\r{' '*70}\r", end="") # Clear the line to print on the same line
        print(f"Problem {prob:03}: {int(round(elapsed_time * 1000)):7} ms{failstr}")

    print(f"Elapsed = {int(total_time)} s, Passed = {num_pass}, Failed = {num_fail}", flush=True)
    os.chdir("..")


ANSWERS_2015: Dict[int, List[str]] = {
	1 : ["74", "1795"],
	2 : ["1588178", "3783758"],
	3 : ["2565", "2639"]
}

ANSWERS_2016: Dict[int, List[str]] = {
	1 : ["252", "143"],
	2 : ["56855", "B3C27"],
	3 : ["917", "1649"]
}

ANSWERS_2017: Dict[int, List[str]] = {
	1 : ["1253", "1278"],
	2 : ["47136", "250"],
	3 : ["552", "330785"]
}

ANSWERS_2018: Dict[int, List[str]] = {
	1 : ["505", "72330"],
	2 : ["7192", "mbruvapghxlzycbhmfqjonsie"],
	3 : ["118322", "1178"]
}

ANSWERS_2019: Dict[int, List[str]] = {
	1 : ["3296269", "4941547"],
	2 : ["3790645", "6577"],
	3 : ["3247", "48054"]
}

ANSWERS_2020: Dict[int, List[str]] = {
	1 : ["445536", "138688160"],
	2 : ["645", "737"],
	3 : ["278", "9709761600"]
}

ANSWERS_2021: Dict[int, List[str]] = {
	1 : ["1624", "1653"],
	2 : ["2073315", "1840311528"],
	3 : ["852500", "1007985"]
}

ANSWERS_2022: Dict[int, List[str]] = {
    1 : ["72240", "210957"],
	2 : ["11666", "12767"],
	3 : ["7845", "2790"],
	4 : ["644", "926"],
	5 : ["DHBJQJCCW", "WJVRLSJJT"],
	6 : ["1850", "2823"],
	7 : ["1583951", "214171"],
	8 : ["1533", "345744"],
	9 : ["6175", "2578"],
	10 : ["13920", "EGLHBLFJ"],
    11 : ["110885", "25272176808"],
    12 : ["370", "363"],
    13 : ["5198", "22344"],
    14 : ["728", "27623"],
    15 : ["6078701", "12567351400528"],
    16 : ["1915", "2772"],
    17 : ["3239", "1594842406882"]
}

ANSWERS_2023: Dict[int, List[str]] = {
    1 : ["54081", "54649"],
	2 : ["2285", "77021"],
	3 : ["554003", "87263515"],
	4 : ["23673", "12263631"],
	5 : ["462648396", "2520479"],
	6 : ["1660968", "26499773"],
	7 : ["253205868", "253907829"],
	8 : ["19241", "9606140307013"],
	9 : ["2043677056", "1062"],
	10 : ["6757", "523"],
    11 : ["10154062", "553083047914"],
    12 : ["7407", "30568243604962"],
    13 : ["32723", "34536"],
    14 : ["110407", "87273"],
    15 : ["510273", "212449"],
    16 : ["7870", "8143"],
    17 : ["638", "748"]
}

ANSWERS_2024: Dict[int, List[str]] = {
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
    15 : ["1479679", "1509780"],
    16 : ["88468", "616"],
    17 : ["[7, 0, 3, 1, 2, 6, 3, 7, 1]", "109020013201563"]
}


if __name__ == "__main__":
    run_tests("2015", ANSWERS_2015)
    run_tests("2016", ANSWERS_2016)
    run_tests("2017", ANSWERS_2017)
    run_tests("2018", ANSWERS_2018)
    run_tests("2019", ANSWERS_2019)
    run_tests("2020", ANSWERS_2020)
    run_tests("2021", ANSWERS_2021)
    run_tests("2022", ANSWERS_2022)
    run_tests("2023", ANSWERS_2023)
    run_tests("2024", ANSWERS_2024)
