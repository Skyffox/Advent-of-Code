# Part 1: Work out the steps to release the most pressure in 30 minutes. What is the most pressure you can release?
# Answer: 1915 

# Part 2: With you and an elephant working together for 26 minutes, what is the most pressure you could release?
# Answer: 2772

# Execution time: 38.413s

def solve2(flow, tunnels):

    states = [(1, "AA", "AA", 0, ("zzz",))]
    seen = {}
    best = 0

    max_flow = sum(flow.values())

    while len(states) > 0:

        current = states.pop()
        time, where, elephant, score, opened_s = current
        opened = {x for x in opened_s}

        if seen.get((time, where, elephant), -1) >= score:
            continue
        seen[(time, where, elephant)] = score

        if time == 26:
            best = max(best, score)
            continue

        # optim: if all valves are working, do nothing
        # with a friend this will happen...
        current_flow = sum(flow.get(where, 0) for where in opened)

        if current_flow >= max_flow:

            new_score = score + current_flow
            while time < 25:
                time += 1
                new_score += current_flow
            new_state = (time + 1, where, elephant, new_score, tuple(opened))
            states.append(new_state)
            continue

        # case 1: we open a valve here
        if flow[where] > 0 and where not in opened:
            opened.add(where)

            # case 1A: and the elephant open its valve too!
            if flow[elephant] > 0 and elephant not in opened:
                opened.add(elephant)

                new_score = score + sum(flow.get(where, 0) for where in opened)
                new_state = (time + 1, where, elephant, new_score, tuple(opened))

                states.append(new_state)

                opened.discard(elephant)

            # case 1B: the elephant goes somewhere
            new_score = score + sum(flow.get(where, 0) for where in opened)
            for option in tunnels[elephant]:
                new_state = (time + 1, where, option, new_score, tuple(opened))
                states.append(new_state)

            opened.discard(where)

        # case 2: we go somewhere else
        for option in tunnels[where]:

            # case 2A: and the elephant open its valve!
            if flow[elephant] > 0 and elephant not in opened:
                opened.add(elephant)

                new_score = score + sum(flow.get(where, 0) for where in opened)
                new_state = (time + 1, option, elephant, new_score, tuple(opened))

                states.append(new_state)

                opened.discard(elephant)

            # case 2B: and the elephant goes somewhere
            new_score = score + sum(flow.get(where, 0) for where in opened)
            for option_e in tunnels[elephant]:
                new_state = (time + 1, option, option_e, new_score, tuple(opened))
                states.append(new_state)

    return best


def solve(flow, tunnels):

    states = [(1, "AA", 0, ("zzz",))]
    seen = {}
    best = 0

    while len(states) > 0:

        current = states.pop()
        time, where, score, opened_s = current
        opened = {x for x in opened_s}

        if seen.get((time, where), -1) >= score:
            continue
        seen[(time, where)] = score

        if time == 30:
            best = max(best, score)
            continue

        # if we open the valve here
        if flow[where] > 0 and where not in opened:

            opened.add(where)
            new_score = score + sum(flow.get(where, 0) for where in opened)
            new_state = (time + 1, where, new_score, tuple(opened))

            states.append(new_state)
            opened.discard(where)

        # if we don't open a valve here
        new_score = score + sum(flow.get(where, 0) for where in opened)
        for option in tunnels[where]:
            new_state = (time + 1, option, new_score, tuple(opened))
            states.append(new_state)

    return best


flow_rates = dict()
options = dict()
with open("inputs/16_input.txt") as f:
    for line in f:
        line = line.strip().split(" ")
        valve = line[1]
        flow = int(line[4].split("=")[1].split(";")[0])
        tunnels = line[9:]
        tunnels = [x.split(",")[0] for x in tunnels]
        
        flow_rates[valve] = flow
        options[valve] = tunnels

solution = solve(flow_rates, options)
solution2 = solve2(flow_rates, options)
print(solution)
print(solution2) # correct solution is 2772
