import sys

def parse_height_map(input_lines):
    """Parse a height map from the given input lines."""
    return [[int(ch) for ch in line[:-1]] for line in input_lines]

def pad_height_map(height_map):
    """Added a box of float('inf')s around the edge of the height map."""
    inf_row = [float('inf') for _ in range(len(height_map[0]) + 2)]
    padded_height_map = [inf_row]
    for line in height_map:
        padded_height_map.append([float('inf')] + line + [float('inf')])
    padded_height_map.append(inf_row)
    return padded_height_map

def is_low_point(height_map, i, j):
    """Check if height_map[i][j] is a low point."""
    return all([
        height_map[i][j] < height_map[i-1][j],
        height_map[i][j] < height_map[i+1][j],
        height_map[i][j] < height_map[i][j-1],
        height_map[i][j] < height_map[i][j+1],
    ])

def get_low_point_indices(height_map):
    """Get all the low point heights from the height map."""
    last_row_index = len(height_map) - 1
    last_col_index = len(height_map[0]) - 1
    for i, row in enumerate(height_map):
        if i == 0 or i == last_row_index:
            continue
        for j, _ in enumerate(row):
            if j == 0 or j == last_col_index:
                continue
            if is_low_point(height_map, i, j):
                yield i, j

def get_low_point_heights(height_map):
    """Get all the low point heights from the height map."""
    for i, j in get_low_point_indices(height_map):
        yield height_map[i][j]

def low_point_risk_level_sum(height_map):
    """Compute the sum of the risk levels of the low points."""
    risk_level_sum = 0
    for height in get_low_point_heights(height_map):
        risk_level_sum += height + 1
    return risk_level_sum

def expand_basin(height_map, i, j, known_members):
    """Recursively expand a basin starting from height_map[i][j]."""
    if height_map[i][j] >= 9:
        return set()
    known_members.add((i,j))
    neighborhood = [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]
    for neighbor_i, neighbor_j in neighborhood:
        if (neighbor_i, neighbor_j) not in known_members:
            known_members |= expand_basin(height_map, neighbor_i, neighbor_j, known_members)
    return known_members

def get_basin_at(height_map, i, j):
    """Get the basin with lowest point at height_map[i][j]."""
    return expand_basin(height_map, i, j, set())

def get_basins(height_map):
    """Get all basins in the height map."""
    for i, j in get_low_point_indices(height_map):
        yield get_basin_at(height_map, i, j)

def three_largest_basins_product(height_map):
    """Get the product of the sizes of the three largest basins."""
    basins = sorted(get_basins(height_map), key=len, reverse=True)
    return len(basins[0]) * len(basins[1]) * len(basins[2])

def main():
    """Day 9 of Advent of Code."""
    height_map = parse_height_map(sys.stdin.readlines())
    height_map = pad_height_map(height_map)
    print(low_point_risk_level_sum(height_map))
    print(three_largest_basins_product(height_map))
  
main()