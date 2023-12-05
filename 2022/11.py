# Part 1: What is the level of monkey business after 20 rounds of stuff-slinging simian shenanigans?
# Answer: 112221

# Part 2: Worry levels are no longer divided by three after each item is inspected; you'll need to find another way to keep your worry levels manageable. 
# Starting again from the initial state in your puzzle input, what is the level of monkey business after 10000 rounds?
# Answer: ???

import copy

def round(data, inspections):
    for monkey in data:
        monkey_nr = monkey[0]
        items = monkey[1]
        operation = monkey[2]
        test = monkey[3]
        test_true = monkey[4]
        test_false = monkey[5]

        if items == []:
            continue

        # print("Monkey", monkey_nr)
        tmp_items = copy.deepcopy(items)
        for item in tmp_items:
            # print("Monkey inspects an item with worry level of", item)
            inspections[monkey_nr] += 1
            if operation[1] == "*":
                if operation[2].isdigit():
                    item *= int(operation[2])
                    # print("Worry level is multiplied by", operation[2], "to", item)
                else:
                    item *= item
                    # print("Worry level is multiplied by itself to", item)
            else:
                if operation[2].isdigit():
                    item += int(operation[2])
                    # print("Worry level is increased by", operation[2], "to", item)
                else:
                    item += item
                    # print("Worry level is increased by itself to", item)

            item = item // 3
            # print("Monkey gets bored with item. Worry level is divided by 3 to", item)
            
            if item % test != 0:
                # print("Current worry level is divisible by", test)
                # print("Item with worry level", item, "is thrown to monkey", test_false)
                data[test_false][1].append(item)
                items.pop(0)
            else:
                # print("Current worry level is not divisible by", test)
                # print("Item with worry level", item, "is thrown to monkey", test_true)
                data[test_true][1].append(item)
                items.pop(0)

    return inspections


# Monkey number, [starting items], operation, test, true, false
data = []
with open("inputs/11_input.txt") as f:
    lines = f.readlines()
    lines = [line.strip() for line in lines]

    items = [x.split(":")[1] for x in lines[1::7]]
    items = [x.split(",") for x in items]
    items = [list(map(int, x)) for x in items]

    operation = [x.split(":")[1] for x in lines[2::7]]
    operation = [x.split("= ")[1] for x in operation]
    operation = [x.split(" ") for x in operation]

    test = list(map(int,[x.split(" ")[3] for x in lines[3::7]]))
    if_true = list(map(int,[x.split(" ")[5] for x in lines[4::7]]))
    if_false = list(map(int,[x.split(" ")[5] for x in lines[5::7]]))
    monkeys = list(range(len(items)))

    for x in range(len(monkeys)):
        lst = [monkeys[x], items[x], operation[x], test[x], if_true[x], if_false[x]]
        data.append(lst)


inspections = [0] * len(data)
for i in range(20):
    # print("After round", i, "the monkeys are holding items with these worry levels:")
    # print([m[1] for m in data])
    inspections = round(data, inspections)

print("Amount of inspections after 20 rounds:", inspections)
largest = max(inspections)
inspections.remove(largest)
second_largest = max(inspections)
print("Multiplication of two most active monkeys:", largest * second_largest)