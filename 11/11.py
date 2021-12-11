import sys
import time
from copy import deepcopy


class Grid:

    def __init__(self, grid):
        self.grid = grid
        self.n_rows = len(grid)
        self.n_cols = 0 if not grid else len(grid[0])
    
    def get(self, i, j):
        return self.grid[i][j]
    
    def set(self, i, j, value):
        self.grid[i][j] = value
    
    def __len__(self):
        return self.n_rows * self.n_cols
    
    def incr(self, i, j):
        """Increment the value at grid[i][j]."""
        self.grid[i][j] += 1

    def __iter__(self):
        for i, row in enumerate(self.grid):
            for j, value in enumerate(row):
                yield i, j, value
    
    def __repr__(self):
        return "".join(["".join(str(energy) for energy in row) + "\n" for row in self.grid])
    
    def copy(self):
        return Grid(deepcopy(self.grid))
    
    def neighborhood(self, i, j):
        """Get the indices in the neighborhood of grid[i][j]."""
        i_deltas = [0]
        j_deltas = [0]
        if i > 0:
            i_deltas.append(-1)
        if i < self.n_rows - 1:
            i_deltas.append(1)
        if j > 0:
            j_deltas.append(-1)
        if j < self.n_cols - 1:
            j_deltas.append(1)
        for i_delta in i_deltas:
            for j_delta in j_deltas:
                # Skip the point that we're looking for the neighborhood of.
                if i_delta == j_delta == 0:
                    continue
                yield i + i_delta, j + j_delta
    
    def update_flash_deltas(self, i, j, deltas):
        """Update the number of times indices in the neighborhood of grid[i][j] have been flashed."""
        for k, l in self.neighborhood(i, j):
            deltas[k][l] += 1
        return deltas


def step(grid):
    """
    Perform one energy change step, mutating the grid.
    
    Returns number of flashes that occured during the step.
    """
    flash_count = 0
    for i, j, _ in grid:
        grid.incr(i, j)
    check_flashes = True
    already_flashed = [[False for _ in range(grid.n_cols)] for _ in range(grid.n_rows)]
    energy_deltas = [[0 for _ in range(grid.n_cols)] for _ in range(grid.n_rows)]
    while check_flashes:
        check_flashes = False
        for i, j, energy in grid:
            if energy > 9:
                grid.update_flash_deltas(i, j, energy_deltas)
                grid.set(i, j, 0)
                already_flashed[i][j] = True
                flash_count += 1
                check_flashes = True
        for i, j, _ in grid:
            if not already_flashed[i][j]:
                new_energy = grid.get(i, j) + energy_deltas[i][j]
                grid.set(i, j, new_energy)
            energy_deltas[i][j] = 0
    return flash_count


def part1(grid):
    """Part 1 of day 11."""
    grid = grid.copy()
    flash_count = 0
    for _ in range(100):
        flash_count += step(grid)
    return flash_count


def part2(grid):
    """Part 2 of day 11."""
    grid = grid.copy()
    step_number = 0
    while True:
        step_number += 1
        if step(grid) == len(grid):
            return step_number


def main():
    """Advent of Code day 11."""
    lines = [[int(n) for n in line[:-1]] for line in sys.stdin.readlines()]
    start_time = time.time()
    grid = Grid(lines)
    print(part1(grid))
    print(part2(grid))
    print(f"Elapsed (no IO): {1000 * (time.time() - start_time)}ms")


main()
