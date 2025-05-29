# pylint: disable=line-too-long
"""
Day 15: Beverage Bandits

Part 1: What is the outcome of the combat described in your puzzle input?
Answer: 216270

Part 2: After increasing the Elves' attack power until it is just barely enough for them to win without any Elves dying, 
        what is the outcome of the combat described in your puzzle input?
Answer: 59339
"""

from typing import List, Tuple
from utils import profiler


class Unit:
    """
    Represents a combat unit (Elf or Goblin) on the battlefield grid.

    Each unit has:
    - A team ('E' for Elf, 'G' for Goblin)
    - A position on the grid (x, y)
    - A fixed attack power (default 3, configurable for Elves in Part 2)
    - Health points (initially 200)

    Units take turns in reading order and can:
    - Move toward enemies
    - Attack adjacent enemies
    """
    def __init__(self, team: str, x: int, y: int, attack: int = 3):
        self.team = team # 'E' for Elf or 'G' for Goblin
        self.x = x
        self.y = y
        self.health = 200
        self.attack = attack

    def __lt__(self, other):
        """
        Enables sorting of units by reading order: top to bottom, then left to right.
        Used to determine turn order in each round.
        """
        return (self.y, self.x) < (other.y, other.x)

    def can_attack(self, other):
        """
        Determines if this unit can attack another unit.
        A unit can attack an enemy that is exactly 1 step away (Manhattan distance = 1).

        Args:
            other (Unit): Another unit to evaluate.

        Returns:
            bool: True if `other` is an adjacent enemy; False otherwise.
        """
        return self.team != other.team and abs(self.x - other.x) + abs(self.y - other.y) == 1

    def attack_priority(self):
        """
        Returns a tuple used to prioritize enemy targets:
        - Lowest health comes first.
        - Then top-to-bottom (lowest y).
        - Then left-to-right (lowest x).

        Returns:
            Tuple[int, int, int]: Sorting key for selecting a target.
        """
        return self.health, self.y, self.x

    def get_attack_target(self, units):
        """
        Finds the best adjacent enemy to attack.

        Selection rules:
        - Only considers enemies that are adjacent (one square away).
        - Prefers the enemy with the lowest health.
        - Breaks ties by reading order (top to bottom, then left to right).

        Returns:
            Unit: The chosen enemy unit to attack, or None if no adjacent enemies exist.
        """
        return min(
            filter(self.can_attack, units),
            key=Unit.attack_priority,
            default=None,
        )

    def bfs_find_targets(self, game) -> List[Tuple[int, int, int, int, int]]:
        """
        Performs a breadth-first search (BFS) to find all reachable squares adjacent to enemies.

        For each adjacent square around the unit, it explores the map using BFS,
        trying to find the shortest path to any square adjacent to an enemy unit.

        The result is a list of candidate paths represented as tuples:
        (distance, enemy_y, enemy_x, move_y, move_x)

        - distance: Steps required to reach the square adjacent to the enemy
        - enemy_y, enemy_x: Position adjacent to the enemy
        - move_y, move_x: First step the unit should take to get there

        Returns:
            List[Tuple[int, int, int, int, int]]: All reachable enemy-adjacent positions and paths.
        """
        paths = []
        for move_x, move_y in adjacent(self.x, self.y):
            if not game.free[move_y][move_x]:
                continue

            visited = set(((self.x, self.y),))
            edges = [(move_x, move_y)]
            visited.add((move_x, move_y))
            distance = 1
            best_distance = None

            while edges:
                new_edges = []
                for edge_x, edge_y in edges:
                    for x, y in adjacent(edge_x, edge_y):
                        if any(
                            unit.x == x and unit.y == y and unit.team != self.team
                            for unit in game.units
                        ):
                            # Found an enemy-adjacent square
                            paths.append((distance, edge_y, edge_x, move_y, move_x))
                            best_distance = distance
                        elif game.free[y][x] and (x, y) not in visited:
                            visited.add((x, y))
                            new_edges.append((x, y))
                edges = new_edges
                distance += 1
                if best_distance and distance > best_distance:
                    break

        return paths

    def tick(self, game):
        """
        Executes a single turn for the unit.

        A full turn consists of:
        1. Checking for adjacent enemies and attacking if possible.
        2. If no enemies are adjacent, using BFS to move toward the nearest reachable enemy.
        3. After moving (if applicable), attempting to attack again.

        Args:
            game (Game): The current game state.
        """
        attack_target = self.get_attack_target(game.units)

        if not attack_target:
            # Use BFS to find reachable target positions
            paths = self.bfs_find_targets(game)

            if paths:
                # Select the best target square to move to
                _, _, _, move_y, move_x = min(paths)

                # Move to the chosen square
                game.free[self.y][self.x] = True
                self.x = move_x
                self.y = move_y
                game.free[self.y][self.x] = False

                # Try to attack after moving
                attack_target = self.get_attack_target(game.units)

        if attack_target:
            # Attack the chosen target
            attack_target.health -= self.attack
            if attack_target.health <= 0:
                game.units.remove(attack_target)
                game.free[attack_target.y][attack_target.x] = True


def adjacent(x: int, y: int) -> List[Tuple[int, int]]:
    """
    Returns the list of coordinates adjacent to the given (x, y) position.

    The returned coordinates follow reading order:
    - Down (x, y+1)
    - Up (x, y-1)
    - Right (x+1, y)
    - Left (x-1, y)

    Args:
        x (int): X-coordinate of the current position.
        y (int): Y-coordinate of the current position.

    Returns:
        List[Tuple[int, int]]: A list of (x, y) tuples for adjacent squares.
    """
    return [(x + dx, y + dy) for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]]


class Game:
    """
    Represents the game state, including the map grid and all units.

    The grid is a 2D boolean matrix where:
    - True indicates a free/open space ('.')
    - False indicates a wall or occupied square ('#', or unit present)

    Units are stored as a list of Unit objects and updated throughout the simulation.
    """
    def __init__(self, data: str, elf_attack: int = 3):
        self.free = []  # 2D grid: True for empty space, False for wall or occupied
        self.units = [] # List of Unit objects
        for y, line in enumerate(data):
            self.free.append([])
            for x, char in enumerate(line):
                self.free[-1].append(char == '.')
                if char == 'E' or char == 'G':
                    attack = elf_attack if char == 'E' else 3
                    self.units.append(Unit(char, x, y, attack))

    def team_size(self, team: str):
        """
        Returns the number of active (alive) units on a given team.

        Args:
            team (str): 'E' for Elves or 'G' for Goblins.

        Returns:
            int: Number of living units on the team.
        """
        return sum(unit.team == team for unit in self.units)

    def team_health(self, team: str):
        """
        Returns the sum of health for all living units on the specified team.

        Args:
            team (str): 'E' for Elves or 'G' for Goblins.

        Returns:
            int: Total remaining health of that team.
        """
        return sum(unit.health for unit in self.units if unit.team == team)


@profiler
def part_one(data: str):
    """
    Simulates the full combat using default attack power (3) for both teams.
    The battle proceeds in rounds until one team is eliminated.

    Outcome is calculated as:
        number of full rounds completed * total remaining health of the winning team

    Args:
        data (str): List of strings representing the map input.

    Returns:
        int: The final combat outcome score.
    """
    game = Game(data)
    time = 0
    while True:
        for unit in sorted(game.units):
            if unit.health > 0:
                if game.team_size('E') == 0:
                    return time * game.team_health('G')
                if game.team_size('G') == 0:
                    return time * game.team_health('E')
                unit.tick(game)
        time += 1


def simulate_combat(data: str, elf_attack: int) -> Tuple[int, bool]:
    """
    Simulates the combat with the given elf attack power.

    Args:
        data: The map as a list of strings.
        elf_attack: Attack power to assign to Elves.

    Returns:
        Tuple[int, bool]: (combat outcome, True if the Elves survived)
    """
    game = Game(data, elf_attack)
    time = 0
    initial_elves = game.team_size('E')

    while True:
        game.units.sort()
        for unit in list(game.units):
            if unit.health <= 0:
                continue
            if game.team_size('G') == 0:
                # Elves win; check if any died
                elves_survived = game.team_size('E') == initial_elves
                return time * game.team_health('E'), elves_survived
            if game.team_size('E') == 0:
                # Goblins win (invalid for part 2)
                return 0, False
            unit.tick(game)
        time += 1


@profiler
def part_two(data: str):
    """
    Solves Part 2 of the problem by finding the minimum Elf attack power
    that allows Elves to win without any casualties.

    The function increments the Elf attack power starting from 4 (since 3
    may result in Elf deaths as observed in Part 1) and simulates the combat
    until a no-Elf-death victory is found.

    Args:
        data (str): The input battlefield map as a list of strings.

    Returns:
        int: The outcome score of the combat (rounds completed * total health)
             for the minimal Elf attack power where no Elves die.
    """
    for elf_attack in range(4, 200):
        outcome, elves_survived = simulate_combat(data, elf_attack)
        if elves_survived:
            return outcome


def get_input(file_path: str) -> List[List[str]]:
    """
    Each line in the file represents a row on the grid.
    Each character is converted into an element of a list, forming a list of lists.

    Args:
        file_path (str): Path to the input file containing the map.

    Returns:
        List[List[str]]: A 2D list where each inner list represents a row of characters.
                         Characters can be '.', '#', 'E', 'G', etc.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [list(line.strip()) for line in file.readlines()]


if __name__ == "__main__":
    grid = get_input("inputs/15_input.txt")

    print(f"Part 1: {part_one(grid)}")
    print(f"Part 2: {part_two(grid)}")
