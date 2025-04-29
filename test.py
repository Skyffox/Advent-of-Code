# pylint: disable=line-too-long
"""
Test suite for the AoC solutions. Since all our modules contain the standard entry point of if __name__ == "__main__" we can not simply run 
the module to get our output. We also can not run the individual functions because they require variable arguments.
So instead I will use the subprocess.run() function to read the stdout of each file in this directory and 
compare that with the answers given by the AoC website.
"""

import subprocess
import time
import os
import fnmatch
import re


def find_file(pattern: str, path: str) -> str:
    """Walk the directory for the 'path' variable and return the file that matches the pattern"""
    for _, _, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                return name
    return ""


def run_tests(year: str, answers: dict[int, list]) -> None:
    """Run all AoC 2018 days and compare the output against the answers"""
    total_time: float = 0.0 # In seconds
    num_pass: int = 0
    num_fail: int = 0
    num_remain: int = len(answers)

    print(f"\nTesting problem for year {year}")
    os.chdir(year)

    for (prob, expect_answers) in sorted(answers.items()):
        start_time: float = time.time()

        # Find file in the current directory that has the following format: dayXX.py
        module = find_file(f'day{prob:02}.py', os.getcwd())

        # Run the entire file as a subprocces and pipe the output to stdout
        output: str = subprocess.run(f'python3 {module}', check=False, capture_output=True, text=True).stdout

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

        num_remain -= 1

        print(f"\r{' '*70}\r", end="")
        print(f"Problem {prob:03}: {int(round(elapsed_time * 1000)):7} ms{failstr}")

    print(f"Elapsed = {int(total_time)} s, Passed = {num_pass}, Failed = {num_fail}, Remaining = {num_remain}", flush=True)
    os.chdir("..")


ANSWERS_2015: dict[int, list] = {
	1 : ["74", "1795"],
	2 : ["1588178", "3783758"],
	3 : ["2565", "2639"]
}

ANSWERS_2016: dict[int, list] = {
	1 : ["252", "143"],
	2 : ["56855", "B3C27"],
	3 : ["917", "1649"]
}

ANSWERS_2017: dict[int, list] = {
	1 : ["1253", "1278"],
	2 : ["47136", "250"],
	3 : ["552", "330785"]
}

ANSWERS_2018: dict[int, list] = {
	1 : ["505", "72330"],
	2 : ["7192", "mbruvapghxlzycbhmfqjonsie"],
	3 : ["118322", "1178"]
}

ANSWERS_2019: dict[int, list] = {
	1 : ["3296269", "4941547"],
	2 : ["3790645", "6577"],
	3 : ["3247", "48054"]
}

ANSWERS_2020: dict[int, list] = {
	1 : ["445536", "138688160"],
	2 : ["645", "737"],
	3 : ["278", "9709761600"]
}

ANSWERS_2021: dict[int, list] = {
	1 : ["1624", "1653"],
	2 : ["2073315", "1840311528"],
	3 : ["852500", "1007985"]
}

ANSWERS_2022: dict[int, list] = {
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

ANSWERS_2023: dict[int, list] = {
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
    # 11 : ["", ""],
    # 12 : ["", ""],
    # 13 : ["", ""],
    # 14 : ["", ""],
    # 15 : ["", ""],
    # 16 : ["", ""],
    # 17 : ["", ""]
}

ANSWERS_2024: dict[int, list] = {
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
    17 : ["[7,0,3,1,2,6,3,7,1]", "109020013201563"]
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
