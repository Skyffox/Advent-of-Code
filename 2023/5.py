# # Part 1: Find the lowest location number for initial seed values.
# # Answer: 462648396

# # Part 2: The second number for seeds is now the range of numbers you need to look over, not just another number.
# # Answer: 2520479


# Map a value to a new value if it is within a certain range.
def custom_map(seed, dest, src, rng):
    if seed in range(src, src + rng + 1):
        return dest + (seed - src), True
    else: 
        return seed, False


with open("inputs/5_input.txt") as f:
    seeds = []
    mappings = []
    single_mapping = []
    for line in f:
        line = line.strip()
        if "seeds:" in line:
            seeds = line.split(":")[1].strip().split(" ")
            input = [[x, False] for x in seeds]

        if line != "" and line[0].isdigit():
            line = line.split(" ")
            dest_range_start = int(line[0])
            src_range_start = int(line[1])
            range_length = int(line[2])

            single_mapping.append((dest_range_start, src_range_start, range_length))

            # Part 1
            for idx, (seed, mapped) in enumerate(input):
                # Only map values that have not been mapped during the same mapping.
                if not mapped:
                    (new_val, is_mapped) = custom_map(int(seed), dest_range_start, src_range_start, range_length)
                    # Update the value and make sure it is not mapped again.
                    if is_mapped:
                        input[idx][0], input[idx][1] = new_val, True
        
        # Set every value being mapped to False once a new mapping starts.
        elif (line != ""):
            for seed in input:
                seed[1] = False
            
            # Add the mapping to a list to later iterate over.
            if single_mapping != []:
                mappings.append(single_mapping)
                single_mapping = []

# Add the last mapping.
mappings.append(single_mapping)
# Create a list where the input seeds are paired.
current_ranges = [(int(seeds[x]), int(seeds[x+1])) for x in range(0, len(seeds) - 1, 2)]

# Part 2
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

print("Lowest location number after mapping:", min(input)[0])
print("Lowest location after seeds have been made into a range:", min([x[0] for x in current_ranges]))