import sys
import time


def ternary_search(f, lb, ub):
    """Find min { f(x) : x \in [lb, ub] } via a ternary search."""
    while lb != ub:
        x1 = int(lb + (ub - lb) / 3 + 0.5)
        x2 = int(lb + 2 * (ub - lb) / 3 + 0.5)
        fx1, fx2 = f(x1), f(x2)
        if fx1 < fx2:
            ub = x2
        elif fx1 > fx2:
            lb = x1
        else:
            lb = x1
            ub = x2
    return f(lb)


def minimize_fuel(input_positions, fuel_func):
    """Given a fuel consumption function, minimize fuel used to align the input positions."""
    min_pos, max_pos = min(input_positions), max(input_positions)
    obj_func = lambda x: sum(fuel_func(x, pos) for pos in input_positions)
    best_obj = ternary_search(obj_func, min_pos, max_pos)
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
    start_time = time.time()
    print(minimize_fuel(input_positions, lambda x, pos: abs(x - pos)))
    triangle_numbers = triangle_number_table(max(input_positions))
    print(minimize_fuel(input_positions, lambda x, pos: triangle_numbers[abs(x - pos)]))
    print(f"Elapsed (no IO): {1000 * (time.time() - start_time):.3f}ms")


main()