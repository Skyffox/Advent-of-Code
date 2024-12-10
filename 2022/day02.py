# Part 1: What would your total score be if everything goes exactly according to your strategy guide?
# Answer: 11666

# Part 2: Following the Elf's instructions for the second column, what would your total score be if everything goes exactly according to your strategy guide?
# Answer: 12767

def part1(player, enemy):
    score = 0
    if enemy == "A":
        if player == "X":
            score += 4
        if player == "Y":
            score += 8
        if player == "Z":
            score += 3

    if enemy == "B":
        if player == "X":
            score += 1
        if player == "Y":
            score += 5
        if player == "Z":
            score += 9

    if enemy == "C":
        if player == "X":
            score += 7
        if player == "Y":
            score += 2
        if player == "Z":
            score += 6

    return score


def part2(outcome, enemy):
    score = 0
    if enemy == "A":
        if outcome == "X":
            score += 3
        if outcome == "Y":
            score += 4
        if outcome == "Z":
            score += 8

    if enemy == "B":
        if outcome == "X":
            score += 1
        if outcome == "Y":
            score += 5
        if outcome == "Z":
            score += 9

    if enemy == "C":
        if outcome == "X":
            score += 2
        if outcome == "Y":
            score += 6
        if outcome == "Z":
            score += 7

    return score

with open("inputs/2_input.txt") as f:
    score1 = 0
    score2 = 0
    for line in f:
        line = line.strip().split(" ")
        enemy = line[0]
        player = line[1]

        score1 += part1(player, enemy)
        score2 += part2(player, enemy)

print("Score according to the strategy guide:", score1)
print("Score according to updated strategy guide:", score2)