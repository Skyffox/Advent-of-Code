# pylint: disable=line-too-long
"""
Part 1: Find the lowest location number for initial seed values
Answer: 462648396

Part 2: The second number for seeds is now the range of numbers you need to look over, not just another number
Answer: 2520479
"""

from utils import profiler


def get_input(file_path: str) -> list:
    """Get the input data"""
    seeds, is_mapped, all_mappings, mappings = [], [], [], []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip().split(" ")
            if "seeds:" in line:
                seeds = line[1:]
                is_mapped = [[x, False] for x in seeds]

            if line != "" and line[0].isdigit():
                mappings.append([int(line[0]), int(line[1]), int(line[2])])
            elif line != "":
                all_mappings.append(mappings)
                mappings = []

    all_mappings.append(mappings)
    return seeds, is_mapped, all_mappings


def custom_map(seed, dest, src, rng):
    """Map a value to a new value if it is within a certain range"""
    if seed in range(src, src + rng + 1):
        return dest + (seed - src), True
    return seed, False


@profiler
def part_1(is_mapped: list, mappings: list) -> int:
    """Every mapping iteration try to map all the seeds to new values, can only be mapped once per iteration"""
    for mapping in mappings:
        # Set every value being mapped to False once a new mapping starts.
        for idx, (seed, mapped) in enumerate(is_mapped):
            is_mapped[idx][1] = False

        for (dest_range_start, src_range_start, range_length) in mapping:
            for idx, (seed, mapped) in enumerate(is_mapped):
                # Only map values that have not been mapped during the same mapping.
                if not mapped:
                    (new_val, is_now_mapped) = custom_map(int(seed), dest_range_start, src_range_start, range_length)
                    # Update the value and make sure it is not mapped again.
                    if is_now_mapped:
                        is_mapped[idx] = [new_val, True]

    return min(is_mapped)[0]


@profiler
def part_2(seeds: list, mappings: list) -> int:
    """The seeds are not individual starting positions but describe a range of numbers"""
    current_ranges = [(int(seeds[x]), int(seeds[x + 1])) for x in range(0, len(seeds) - 1, 2)]

    for mapping in mappings:
        mapped_ranges = []
        unmapped_ranges = current_ranges

        # Iterate over a mapping.
        for map_dst, map_src, map_len in mapping:
            new_unmapped_ranges = []

            # Take a seed pair.
            for start, count in unmapped_ranges:
                # If the seed start is smaller than the mapping then the range that will be unmapped will
                # either be the entire seed range or from the seed start to the start of the mapping.
                if start < map_src:
                    new_unmapped_ranges.append((start, min(count, map_src - start)))

                # The seed range is larger than the mapping range.
                if start + count > map_src + map_len:
                    new_start = max(start, map_src + map_len)
                    new_unmapped_ranges.append((new_start, start + count - new_start))

                # Find what range of the current seed lies within the mapped range.
                # Then add the mapped value together with the range that was found.
                intersect_start = max(start, map_src)
                intersect_len = min(start + count, map_src + map_len) - intersect_start
                if intersect_len > 0:
                    mapped_ranges.append((intersect_start + (map_dst - map_src), intersect_len))

            # Do the checks again only for unmapped ranges of a seed.
            unmapped_ranges = new_unmapped_ranges
        # The mapping starts again so update the ranges to iterate over.
        current_ranges = unmapped_ranges + mapped_ranges

    return min([x[0] for x in current_ranges])


if __name__ == "__main__":
    seed_input, is_mapped_input, mappings_input = get_input("inputs/5_input.txt")

    print(f"Part 1: {part_1(is_mapped_input, mappings_input)}")
    print(f"Part 2: {part_2(seed_input, mappings_input)}")
