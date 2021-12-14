import sys
from collections import defaultdict


def parse_input(lines):
    """Parse the problem input."""
    polymer_template = lines[0].rstrip()
    insertion_rules = {}
    for line in lines[2:]:
        adjacents, insert = line.rstrip().split(" -> ")
        insertion_rules[adjacents] = insert
    return polymer_template, insertion_rules


def additive_update(dict_to_update, other_dict):
    """Additively update a dict with the contents of another dict."""
    for k, v in other_dict.items():
        dict_to_update[k] += v


def elem_counts(polymer, step, insertion_rules, table):
    """Count the number of time each element occurs after the given number of insertion steps."""
    counts = defaultdict(int)
    for index, (x, y) in enumerate(zip(polymer, polymer[1:])):
        additive_update(counts, _elem_counts(x+y, step, insertion_rules, table))
        if index > 0:
            counts[x] -= 1
    return counts


def _elem_counts(polymer, step, insertion_rules, table):
    """Count the number of time each element occurs using dynamic programming."""
    if table[polymer][step]:
        return table[polymer][step]
    if step == 0:
        table[polymer][0] = {polymer[0]: 2} if polymer[0] == polymer[1] else {polymer[0]: 1, polymer[1]: 1}
        return table[polymer][step]
    counts = defaultdict(int)
    x, z = polymer
    y = insertion_rules[x+z]
    additive_update(counts, _elem_counts(x+y, step-1, insertion_rules, table))
    additive_update(counts, _elem_counts(y+z, step-1, insertion_rules, table))
    counts[y] -= 1
    table[polymer][step] = counts
    return counts


def init_table():
    """Initialize the dynamic programming table."""
    return defaultdict(lambda: defaultdict(lambda: None))


def min_max_diff(ls):
    """Get the difference between the min and max values in the list."""
    return max(ls) - min(ls)


def main():
    """Advent of Code day 14."""
    polymer_template, insertion_rules = parse_input(sys.stdin.readlines())
    table = init_table()
    counts_pt1 = elem_counts(polymer_template, 10, insertion_rules, table)
    print(min_max_diff(counts_pt1.values()))
    counts_pt2 = elem_counts(polymer_template, 40, insertion_rules, table)
    print(min_max_diff(counts_pt2.values()))


main()