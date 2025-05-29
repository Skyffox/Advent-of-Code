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
	3 : ["2565", "2639"],
    4 : ["117946", "3938038"],
    5 : ["236", "51"],
	6 : ["543903", "14687245"],
	7 : ["16076", "2797"],
	8 : ["1333", "2046"],
	9 : ["251", "898"],
	10 : ["492982", "6989950"],
    11 : ["vzbxxyzz", "vzcaabcc"],
    12 : ["111754", "65402"],
    13 : ["664", "640"],
    14 : ["2655", "1059"],
    15 : ["18965440", "15862900"],
    16 : ["373", "260"],
    17 : ["4372", "4"]
}

ANSWERS_2016: Dict[int, List[str]] = {
	1 : ["252", "143"],
	2 : ["56855", "B3C27"],
	3 : ["917", "1649"],
    4 : ["245102", "324"],
    5 : ["2414bc77", "437e60fc"],
	6 : ["wkbvmikb", "evakwaga"],
	7 : ["110", "242"],
	8 : ["110", "ZJHRKCPLYJ"],
	9 : ["97714", "10762972461"],
	10 : ["157", "1085"],
    11 : ["47", "71"],
    12 : ["317993", "9227647"],
    13 : ["92", "124"],
    14 : ["23769", "20606"],
    15 : ["16824", "3543984"],
    16 : ["10111110010110110", "01101100001100100"],
    17 : ["RDRLDRDURD", "596"]
}

ANSWERS_2017: Dict[int, List[str]] = {
	1 : ["1253", "1278"],
	2 : ["47136", "250"],
	3 : ["552", "330785"],
    4 : ["451", "223"],
    5 : ["373543", "27502966"],
	6 : ["3156", "1610"],
	7 : ["dtacyn", "521"],
	8 : ["3745", "4644"],
	9 : ["14212", "6569"],
	10 : ["46600", "23234babdc6afa036749cfa9b597de1b"],
    11 : ["824", "1548"],
    12 : ["152", "186"],
    13 : ["1316", "3840052"],
    14 : ["8216", "1139"],
    15 : ["592", "320"],
    16 : ["gkmndaholjbfcepi", "abihnfkojcmegldp"],
    17 : ["808", "47465686"]
}

ANSWERS_2018: Dict[int, List[str]] = {
	1 : ["505", "72330"],
	2 : ["7192", "mbruvapghxlzycbhmfqjonsie"],
	3 : ["118322", "1178"],
    4 : ["19830", "43695"],
    5 : ["11668", "4652"],
	6 : ["4398", "39560"],
	7 : ["BKCJMSDVGHQRXFYZOAULPIEWTN", "1040"],
	8 : ["36307", "25154"],
	9 : ["384475", "3187566597"],
	10 : ["BFFZCNXE", "10391"],
    11 : ["21,93", "231,108,14"],
    12 : ["1184", "250000000219"],
    13 : ["118,112", "50,21"],
    14 : ["8176111038", "20225578"],
    15 : ["216270", "59339"],
    16 : ["607", "577"],
    17 : ["30384", "24479"]
}

ANSWERS_2019: Dict[int, List[str]] = {
	1 : ["3296269", "4941547"],
	2 : ["3790645", "6577"],
	3 : ["3247", "48054"],
    4 : ["594", "364"],
    5 : ["4511442", "12648139"],
	6 : ["270768", "451"],
	7 : ["440880", "3745599"],
	8 : ["2193", "YEHEF"],
	9 : ["3497884671", "46470"],
	10 : ["292", "317"],
    11 : ["2319", "UERPRFGJ"],
    12 : ["7138", "572087463375796"],
    13 : ["306", "15328"],
    14 : ["1185296", "1376631"],
    15 : ["230", "288"],
    16 : ["84970726", "47664469"],
    17 : ["3660", "962913"]
}

ANSWERS_2020: Dict[int, List[str]] = {
	1 : ["445536", "138688160"],
	2 : ["645", "737"],
	3 : ["278", "9709761600"],
    4 : ["192", "101"],
    5 : ["892", "625"],
	6 : ["6457", "3260"],
	7 : ["272", "172246"],
	8 : ["1930", "1688"],
	9 : ["18272118", "2186361"],
	10 : ["1904", "10578455953408"],
    11 : ["2283", "2054"],
    12 : ["1457", "106860"],
    13 : ["222", "408270049879073"],
    14 : ["11327140210986", "2308180581795"],
    15 : ["1428", "3718541"],
    16 : ["19087", "1382443095281"],
    17 : ["276", "2136"]
}

ANSWERS_2021: Dict[int, List[str]] = {
	1 : ["1624", "1653"],
	2 : ["2073315", "1840311528"],
	3 : ["852500", "1007985"],
    4 : ["11536", "1284"],
    5 : ["5585", "17193"],
	6 : ["362666", "1640526601595"],
	7 : ["344297", "97164301"],
	8 : ["272", "1007675"],
	9 : ["500", "970200"],
	10 : ["442131", "3646451424"],
    11 : ["1647", "348"],
    12 : ["3563", "105453"],
    13 : ["745", "ABKJFBGC"],
    14 : ["3247", "4110568157153"],
    15 : ["824", "3063"],
    16 : ["875", "1264857437203"],
    17 : ["13203", "5644"]
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
