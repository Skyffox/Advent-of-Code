# Part 1: See if the game is valid by comparing pulled cubes with set maximum.
# Answer: 2285

# Part 2: See what the maximum amount of cubes is needed to play every game.
# Answer: 77021

maximums = {'red' : 12, 'green' : 13, 'blue' : 14}
possible_totals = 0
totals_part2 = 0

with open("inputs/2_input.txt") as f:
    for line in f:
        line = line.strip().split(":")
        game = line[0].split(" ")[1] # Separates the game number from the input
        input = line[1].split(";")
        
        valid_input = True
        max_red = 0
        max_green = 0
        max_blue = 0

        for i in input:
            moves = i.split(",")
            for move in moves:
                move = move.strip().split(" ")
                if int(move[0]) > maximums[move[1]]:
                    valid_input = False
        
                # Part 2
                if move[1] == 'red':
                    max_red = max(max_red, int(move[0]))
                if move[1] == 'green':
                    max_green = max(max_green, int(move[0]))
                if move[1] == 'blue':
                    max_blue = max(max_blue, int(move[0]))

        totals_part2 += (max_red * max_green * max_blue)

        if (valid_input):
            possible_totals += int(game)
        
print("Sum of IDs that are possible with maximum cubes (according to variable maximums):", possible_totals)
print("Sum of the power of sets of cubes that make all games possible:", totals_part2)