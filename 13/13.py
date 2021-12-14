import sys


def parse_fold(line):
    """Parse a fold instruction."""
    words, number = line.split("=")
    axis = words[-1]
    number = int(number)
    return axis, number


def parse_coordinate(line):
    """Parse a coordinate."""
    x, y = line.split(",")
    return int(x), int(y)


def parse_input(lines):
    """Parse the puzzle input."""
    coordinates = []
    folds = []
    parsing_folds = False
    for line in lines:
        if line == "\n":
            parsing_folds = True
            continue
        if parsing_folds:
            folds.append(parse_fold(line))
        else:
            coordinates.append(parse_coordinate(line))
    return coordinates, folds


def build_grid(coordinates):
    """Build a grid from the given coordinates."""
    max_x = max_y = 0
    for x, y in coordinates:
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y
    grid = [[0 for _ in range(max_x+1)] for _ in range(max_y+1)]
    for x, y in coordinates:
        grid[y][x] = 1
    return grid


def perform_fold_y(grid, fold_index):
    """Perform a fold across a line perpendicular to the y-axis."""
    top_half = grid[:fold_index]
    bottom_half = grid[fold_index+1:]
    folded_section = []
    for top_line, bottom_line in zip(reversed(top_half), bottom_half):
        folded_section.append(
            [top_val or bottom_val for top_val, bottom_val in zip(top_line, bottom_line)])
    lowest_unfolded_line = fold_index - len(folded_section)
    grid[lowest_unfolded_line:fold_index] = reversed(folded_section)
    del grid[fold_index:]
    return grid


def perform_fold_x(grid, fold_index):
    """Perform a fold across a line perpendicular to the x-axis."""
    grid = [list(col) for col in zip(*grid)]
    grid = perform_fold_y(grid, fold_index)
    return [list(row) for row in zip(*grid)]


def perform_fold(grid, fold):
    """Perform the given fold on the grid."""
    fold_axis, fold_index = fold
    if fold_axis == "x":
        grid = perform_fold_x(grid, fold_index)
    elif fold_axis == "y":
        grid = perform_fold_y(grid, fold_index)
    return grid


def count_visible_dots(grid):
    """Count the number of visible dots in the grid."""
    return sum(sum(row) for row in grid)


def grid_string(grid):
    """Get a string representation of a grid."""
    row_strings = []
    last_row = len(grid) - 1
    for i, row in enumerate(grid):
        row_string = "".join("#" if n == 1 else "." for n in row)
        if i < last_row:
            row_string = row_string + "\n"
        row_strings.append(row_string)
    return "".join(row_strings)


def main():
    """Advent of Code Day 13."""
    coordinates, folds = parse_input(sys.stdin.readlines())
    grid = build_grid(coordinates)
    grid = perform_fold(grid, folds[0])
    print(count_visible_dots(grid))
    for fold in folds[1:]:
        grid = perform_fold(grid, fold)
    print(grid_string(grid))


main()