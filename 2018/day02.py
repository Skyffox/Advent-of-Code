# Part 1: Calculate the checksum of IDs that contain two of any letter or three of any letter
# Answer: 7192

# Part 2: Find the two IDs that are matching but off by one
# Answer: mbruvapghxlzycbhmfqjonsie

doubles_count = 0
triples_count = 0
lst = []
with open("inputs/2_input.txt") as f:
    for line in f:
        inp = list(line.strip())
        lst.append(inp)
        
        # Part 1
        # Count the occurence of every letter in the string
        occurences = [inp.count(x) for x in set(inp)]
                
        if 2 in occurences:
            doubles_count += 1
        if 3 in occurences:
            triples_count += 1

# Part 2
for idx, lst1 in enumerate(lst):
    for lst2 in lst[idx:]:
        # Return True or False for each comparison between two lists
        # If there is one False then we have a match
        matches = [lst1[idx] == lst2[idx] for idx in range(len(lst1))]
        if matches.count(False) == 1:
            wrong_index = matches.index(False)
            tmp = lst1[::]
            tmp.pop(wrong_index)

print("Part 1:", doubles_count * triples_count)
print("Part 2:", "".join(tmp))