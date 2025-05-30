# pylint: disable=line-too-long
"""
Day 4: Passport Processing

Part 1: Count the number of valid passports - those that have all required fields. Treat cid as optional. How many passports are valid?
Answer: 192

Part 2: Count the number of valid passports - those that have all required fields and valid values. 
        Continue to treat cid as optional. In your batch file, how many passports are valid?
Answer: 101
"""

from typing import List, Dict
import re
from utils import profiler


def get_input(file_path: str) -> List[Dict[str, str]]:
    """
    Reads the input file and parses it into a list of passport dictionaries.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        List[Dict[str, str]]: A list of dictionaries representing passports.
    """
    passports = []
    passport = {}

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:
                fields = line.split()
                for field in fields:
                    key, value = field.split(":")
                    passport[key] = value
            else:
                passports.append(passport)
                passport = {}

    if passport: # Add last passport if file didn't end with newline
        passports.append(passport)

    return passports


@profiler
def part_one(passports: List[dict]) -> int:
    """
    Counts how many passports have all the required fields.

    The required fields are: byr, iyr, eyr, hgt, hcl, ecl, pid.
    This function checks only the presence of these fields, not their validity.

    Args:
        passports (List[dict]): List of passport dictionaries to validate.

    Returns:
        int: Number of passports containing all required fields.
    """
    required_fields = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
    valid_count = 0

    for passport in passports:
        if required_fields <= passport.keys():
            valid_count += 1

    return valid_count


@profiler
def part_two(passports: List[dict]) -> int:
    """
    Counts how many passports are valid including field value validation.

    Checks for presence of all required fields and validates each field:
    - byr: four digits; 1920 <= byr <= 2002
    - iyr: four digits; 2010 <= iyr <= 2020
    - eyr: four digits; 2020 <= eyr <= 2030
    - hgt: number + "cm" or "in"; 150-193 cm or 59-76 in
    - hcl: a '#' followed by exactly six hex chars
    - ecl: one of specified eye colors
    - pid: a nine-digit number, including leading zeroes

    Args:
        passports (List[dict]): List of passport dictionaries to validate.

    Returns:
        int: Number of passports that pass all validation checks.
    """
    required_fields = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}

    def is_valid(passport):
        try:
            # Validate birth year
            byr = 1920 <= int(passport["byr"]) <= 2002
            # Validate issue year
            iyr = 2010 <= int(passport["iyr"]) <= 2020
            # Validate expiration year
            eyr = 2020 <= int(passport["eyr"]) <= 2030

            # Validate height with units
            hgt = (
                (passport["hgt"].endswith("cm") and 150 <= int(passport["hgt"][:-2]) <= 193)
                or
                (passport["hgt"].endswith("in") and 59 <= int(passport["hgt"][:-2]) <= 76)
            )

            # Validate hair color format
            hcl = bool(re.match(r"^#[0-9a-f]{6}$", passport["hcl"]))

            # Validate eye color membership
            ecl = passport["ecl"] in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}

            # Validate passport ID format
            pid = bool(re.match(r"^\d{9}$", passport["pid"]))

            return byr and iyr and eyr and hgt and hcl and ecl and pid

        except KeyError:
            # Missing required field(s)
            return False

    valid_count = 0

    for passport in passports:
        # Check required fields present and validate values
        if required_fields <= passport.keys() and is_valid(passport):
            valid_count += 1

    return valid_count


if __name__ == "__main__":
    input_data = get_input("inputs/4_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
