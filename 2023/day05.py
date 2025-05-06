# pylint: disable=line-too-long
"""
Part 1: Find the lowest location number for initial seed values  
Answer: 462648396

Part 2: The second number for seeds is now the range of numbers you need to look over, not just another number  
Answer: 2520479
"""

from typing import List, Tuple
from utils import profiler


def get_input(file_path: str) -> Tuple[List[str], List[Tuple[int, bool]], List[List[Tuple[int, int, int]]]]:
    """
    Parse the input file and extract seeds and mapping ranges.

    Args:
        file_path (str): Path to the input file.

    Returns:
        Tuple containing:
            - seeds (List[str]): List of seed numbers as strings.
            - is_mapped (List[Tuple[int, bool]]): List of seed values paired with a mapping flag.
            - all_mappings (List[List[Tuple[int, int, int]]]): Nested list of mapping rules per section.
    """
    seeds: List[str] = []
    is_mapped: List[Tuple[int, bool]] = []
    all_mappings: List[List[Tuple[int, int, int]]] = []
    mappings: List[Tuple[int, int, int]] = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip().split()
            if not line:
                continue
            if line[0] == "seeds:":
                seeds = line[1:]
                is_mapped = [(int(x), False) for x in seeds]
            elif line[0].isdigit():
                mappings.append((int(line[0]), int(line[1]), int(line[2])))
            else:
                if mappings:
                    all_mappings.append(mappings)
                    mappings = []

    if mappings:
        all_mappings.append(mappings)

    return seeds, is_mapped, all_mappings


def custom_map(seed: int, dest: int, src: int, rng: int) -> Tuple[int, bool]:
    """
    Attempt to map a seed to a destination based on a source range.

    Args:
        seed (int): Seed value.
        dest (int): Destination start.
        src (int): Source start.
        rng (int): Range length.

    Returns:
        Tuple[int, bool]: New value and a flag indicating whether it was mapped.
    """
    if src <= seed <= src + rng:
        return dest + (seed - src), True
    return seed, False


@profiler
def part_1(is_mapped: List[Tuple[int, bool]], mappings: List[List[Tuple[int, int, int]]]) -> int:
    """
    Apply all mapping layers to each seed value once per layer.

    Args:
        is_mapped (List[Tuple[int, bool]]): Seed values and their mapping status.
        mappings (List[List[Tuple[int, int, int]]]): Mapping rules.

    Returns:
        int: Minimum mapped value after all transformations.
    """
    for layer in mappings:
        # Reset mapping status at the start of each layer
        is_mapped = [(val, False) for val, _ in is_mapped]

        for dst, src, length in layer:
            for i, (seed, was_mapped) in enumerate(is_mapped):
                if not was_mapped:
                    new_val, mapped = custom_map(seed, dst, src, length)
                    if mapped:
                        is_mapped[i] = (new_val, True)

    return min(val for val, _ in is_mapped)


@profiler
def part_2(seeds: List[str], mappings: List[List[Tuple[int, int, int]]]) -> int:
    """
    Handle seed ranges and determine the lowest final mapped value.

    Args:
        seeds (List[str]): Raw seed values, in start/count pairs.
        mappings (List[List[Tuple[int, int, int]]]): Mapping layers.

    Returns:
        int: Minimum mapped value after processing all ranges.
    """
    current_ranges: List[Tuple[int, int]] = [
        (int(seeds[i]), int(seeds[i + 1])) for i in range(0, len(seeds) - 1, 2)
    ]

    for layer in mappings:
        mapped: List[Tuple[int, int]] = []
        unmapped: List[Tuple[int, int]] = current_ranges

        for dst, src, length in layer:
            new_unmapped = []

            for start, size in unmapped:
                # If the seed start is smaller than the mapping then the range that will be unmapped will
                # either be the entire seed range or from the seed start to the start of the mapping.
                if start < src:
                    new_unmapped.append((start, min(size, src - start)))

                # The seed range is larger than the mapping range.
                if start + size > src + length:
                    new_start = max(start, src + length)
                    new_unmapped.append((new_start, start + size - new_start))

                # Find what range of the current seed lies within the mapped range.
                # Then add the mapped value together with the range that was found.
                intersect_start = max(start, src)
                intersect_len = min(start + size, src + length) - intersect_start
                if intersect_len > 0:
                    mapped.append((intersect_start + (dst - src), intersect_len))

            # Do the checks again only for unmapped ranges of a seed.
            unmapped = new_unmapped
        # The mapping starts again so update the ranges to iterate over.
        current_ranges = mapped + unmapped

    return min(start for start, _ in current_ranges)


if __name__ == "__main__":
    seed_input, is_mapped_input, mappings_input = get_input("inputs/5_input.txt")

    print(f"Part 1: {part_1(is_mapped_input, mappings_input)}")
    print(f"Part 2: {part_2(seed_input, mappings_input)}")
