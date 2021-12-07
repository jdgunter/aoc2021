import sys


def minimize_fuel(input_positions, fuel_func):
    """Given a fuel consumption function, minimize fuel used to align the input positions."""
    best_obj, min_pos, max_pos = float('inf'), min(input_positions), max(input_positions)
    for x in range(min_pos, max_pos+1):
        obj_val = sum(fuel_func(x, pos) for pos in input_positions)
        if obj_val < best_obj:
            best_obj = obj_val
    return best_obj


def triangle_number_table(n):
    """Build a table of the 0th to nth triangle numbers."""
    table = [0] * (n+1)
    for i in range(1, n+1):
        table[i] = i + table[i-1]
    return table


def main():
    """Advent of Code day 7."""
    input_positions = [int(n) for n in sys.stdin.read().split(",")]
    print(minimize_fuel(input_positions, lambda x, pos: abs(x - pos)))
    triangle_numbers = triangle_number_table(max(input_positions))
    print(minimize_fuel(input_positions, lambda x, pos: triangle_numbers[abs(x - pos)]))


main()