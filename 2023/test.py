test1 = []
with open("test.txt") as f:
    for line in f:
        line = line.strip()
        test1.append(line)

test2 = []
with open("test2.txt") as f:
    for line in f:
        line = line.strip()
        test2.append(line)


print(len(test1), len(test2))
for i in range(0, len(test2)):
    if test1[i] != test2[i]:
        print(i, test1[i], test2[i])
        break
