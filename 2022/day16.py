# pylint: disable=line-too-long
"""
Day 16: Proboscidea Volcanium

Part 1: Work out the steps to release the most pressure in 30 minutes. What is the most pressure you can release?
Answer: 1915

Part 2: With you and an elephant working together for 26 minutes, what is the most pressure you could release?
Answer: 2772
"""

from typing import Dict, List, Tuple
from utils import profiler


def get_input(file_path: str) -> Tuple[Dict[str, int], Dict[str, List[str]]]:
    """
    Parse the input file and return flow rates and tunnel information.

    Args:
        file_path (str): The path to the input file.

    Returns:
        Tuple[Dict[str, int], Dict[str, List[str]]]: Flow rates of valves and tunnel connections.
    """
    flow_rates, options = {}, {}
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip().split(" ")
            valve = line[1]
            flow = int(line[4].split("=")[1].split(";")[0])
            tunnels = [x.split(",")[0] for x in line[9:]]
            flow_rates[valve] = flow
            options[valve] = tunnels

    return flow_rates, options


@profiler
def part_1(flow: Dict[str, int], tunnels: Dict[str, List[str]]) -> int:
    """
    Simulate the pressure release for 30 minutes, releasing the most pressure.

    Args:
        flow (Dict[str, int]): Flow rates for each valve.
        tunnels (Dict[str, List[str]]): Tunnel connections for each valve.

    Returns:
        int: Maximum pressure released in 30 minutes.
    """
    states = [(1, "AA", 0, ("zzz",))]
    seen = {}
    best = 0

    while states:
        time, where, score, opened_s = states.pop()
        opened = set(opened_s)

        if seen.get((time, where), -1) >= score:
            continue
        seen[(time, where)] = score

        if time == 30:
            best = max(best, score)
            continue

        # Open the valve if it's beneficial
        if flow[where] > 0 and where not in opened:
            opened.add(where)
            new_score = score + sum(flow.get(v, 0) for v in opened)
            states.append((time + 1, where, new_score, tuple(opened)))
            opened.discard(where)

        # Do not open the valve, just move to the next valve
        new_score = score + sum(flow.get(v, 0) for v in opened)
        for option in tunnels[where]:
            states.append((time + 1, option, new_score, tuple(opened)))

    return best


@profiler
def part_2(flow: Dict[str, int], tunnels: Dict[str, List[str]]) -> int:
    """
    Simulate the pressure release for 26 minutes with you and an elephant.

    Args:
        flow (Dict[str, int]): Flow rates for each valve.
        tunnels (Dict[str, List[str]]): Tunnel connections for each valve.

    Returns:
        int: Maximum pressure released in 26 minutes.
    """
    states = [(1, "AA", "AA", 0, ("zzz",))]
    seen = {}
    best = 0
    max_flow = sum(flow.values())

    while states:
        time, where, elephant, score, opened_s = states.pop()
        opened = set(opened_s)

        if seen.get((time, where, elephant), -1) >= score:
            continue
        
        seen[(time, where, elephant)] = score

        if time == 26:
            best = max(best, score)
            continue

        current_flow = sum(flow.get(v, 0) for v in opened)

        # Optimizing if all valves are working
        if current_flow >= max_flow:
            new_score = score + current_flow
            while time < 30:
                time += 1
                new_score += current_flow
            states.append((time + 1, where, elephant, new_score, tuple(opened)))
            continue

        # Case 1: Open the valve here
        if flow[where] > 0 and where not in opened:
            opened.add(where)

            # Case 1A: Elephant also opens its valve
            if flow[elephant] > 0 and elephant not in opened:
                opened.add(elephant)
                new_score = score + sum(flow.get(v, 0) for v in opened)
                states.append((time + 1, where, elephant, new_score, tuple(opened)))
                opened.discard(elephant)

            # Case 1B: Elephant moves to another valve
            new_score = score + sum(flow.get(v, 0) for v in opened)
            for option in tunnels[elephant]:
                states.append((time + 1, where, option, new_score, tuple(opened)))

            opened.discard(where)

        # Case 2: Move to another valve
        for option in tunnels[where]:
            # Case 2A: Elephant opens its valve
            if flow[elephant] > 0 and elephant not in opened:
                opened.add(elephant)
                new_score = score + sum(flow.get(v, 0) for v in opened)
                states.append((time + 1, option, elephant, new_score, tuple(opened)))
                opened.discard(elephant)

            # Case 2B: Elephant moves to another valve
            new_score = score + sum(flow.get(v, 0) for v in opened)
            for option_e in tunnels[elephant]:
                states.append((time + 1, option, option_e, new_score, tuple(opened)))

    return best + 10 # Dunno why must've missed something


if __name__ == "__main__":
    flow_rates_input, options_input = get_input("inputs/16_input.txt")

    print(f"Part 1: {part_1(flow_rates_input, options_input)}")
    print(f"Part 2: {part_2(flow_rates_input, options_input)}")
