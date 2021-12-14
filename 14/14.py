import sys
from collections import defaultdict


class Polymer:

    class Node:

        def __init__(self, element, next):
            self.element = element
            self.next = next
    
    def __init__(self, polymer_string):
        prev_node = None
        for ch in reversed(polymer_string):
            current_node = self.Node(ch, prev_node)
            prev_node = current_node
        self.polymer = current_node
    
    def rewrite(self, insertion_rules):
        self._rewrite(self.polymer, insertion_rules)
    
    @staticmethod
    def _rewrite(current_node, insertion_rules):
        next_node = current_node.next
        while next_node is not None:
            key = current_node.element + next_node.element
            if key in insertion_rules:
                new_node = Polymer.Node(insertion_rules[key], next_node)
                current_node.next = new_node
            current_node = next_node
            next_node = current_node.next
    
    def __iter__(self):
        current_node = self.polymer
        while current_node != None:
            yield current_node.element
            current_node = current_node.next

    def __str__(self):
        return "".join(list(self))


def parse_input(lines):
    """Parse the problem input."""
    polymer_template = lines[0].rstrip()
    insertion_rules = {}
    for line in lines[2:]:
        adjacents, insert = line.rstrip().split(" -> ")
        insertion_rules[adjacents] = insert
    return polymer_template, insertion_rules


def mce_lce_count(polymer):
    """Get the most common element and least common element counts."""
    element_counts_dict = defaultdict(int)
    for elem in polymer:
        element_counts_dict[elem] += 1
    sorted_element_counts = sorted(element_counts_dict.values())
    return sorted_element_counts[-1], sorted_element_counts[0]


def main():
    """Advent of Code Day 14."""
    polymer_template, insertion_rules = parse_input(sys.stdin.readlines())
    polymer = Polymer(polymer_template)
    # Part 1.
    for _ in range(10):
        polymer.rewrite(insertion_rules)
    most_common_elem_count, least_common_elem_count = mce_lce_count(polymer)
    print(most_common_elem_count - least_common_elem_count)
    # Part 2 intractable via this algorithm.


main()