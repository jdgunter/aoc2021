import sys
from dataclasses import dataclass
from math import ceil, floor
from typing import List, Union


def is_leaf(snailfish_number):
    """Returns True if the given snailfish number is a leaf node."""
    return isinstance(snailfish_number, int)


@dataclass
class SnailfishNumber:
    left: Union[int, 'SnailfishNumber']
    right: Union[int, 'SnailfishNumber']
    parent: 'SnailfishNumber'

    @classmethod
    def make(cls, pair: List[Union[int, List]], parent=None):
        """Make a snailfish number from a list."""
        assert len(pair) == 2
        root = SnailfishNumber(None, None, parent=parent)
        root.left = pair[0] if is_leaf(pair[0]) else SnailfishNumber.make(pair[0], parent=root)
        root.right = pair[1] if is_leaf(pair[1]) else SnailfishNumber.make(pair[1], parent=root)
        return root

    def unmake(self):
        """Unmake a snailfish number into a list."""
        left = self.left if is_leaf(self.left) else self.left.unmake()
        right = self.right if is_leaf(self.right) else self.right.unmake()
        return [left, right]
        

    def __str__(self):
        return str(self.unmake())
        


def leftmost_pair_satisfying(snailfish_number, predicate, state=None, state_func=lambda _: None):
    """
    Find the leftmost snailfish number pair satisfying the given predicate.
    
    Returns the found snailfish number and the result of applying the predicate to the snailfish 
    number and state. 
    """
    if is_leaf(snailfish_number):
        return None, False
    # Check the left side.
    if is_leaf(snailfish_number.left):
        predicate_result = predicate(snailfish_number, state)
        if predicate_result:
            return snailfish_number, predicate_result
    left_number, left_result = leftmost_pair_satisfying(snailfish_number.left, predicate, state_func(state), state_func)
    if left_result:
        return left_number, left_result
    # Now check right side.
    if is_leaf(snailfish_number.right):
        predicate_result = predicate(snailfish_number, state)
        if predicate_result:
            return snailfish_number, predicate_result
    return leftmost_pair_satisfying(snailfish_number.right, predicate, state_func(state), state_func)


def leftmost_exploding_pair(snailfish_number):
    """
    Find the leftmost exploding pair.
    
    A pair is exploding if it is nested inside four pairs.
    """
    
    def is_exploding(snailfish_number, depth):
        return is_leaf(snailfish_number.left) and is_leaf(snailfish_number.right) and depth >= 4
    
    return leftmost_pair_satisfying(snailfish_number, is_exploding, 0, lambda depth: depth + 1)


def leftmost_splitting_number(snailfish_number):
    """Find the leftmost splitting number."""

    def has_splitting_number(snailfish_num, _):
        if is_leaf(snailfish_num.left) and snailfish_num.left >= 10:
            return "left"
        elif is_leaf(snailfish_num.right) and snailfish_num.right >= 10:
            return "right"
        return False
    
    return leftmost_pair_satisfying(snailfish_number, has_splitting_number)


INVERT = {"left": "right", "right": "left"}


def lowest_ancestor_from(snailfish_number, in_direction):
    """Finds the lowest ancestor reached after travelling in the given direction."""
    if snailfish_number.parent is None:
        return None
    if snailfish_number is getattr(snailfish_number.parent, in_direction):
        return snailfish_number.parent
    return lowest_ancestor_from(snailfish_number.parent, in_direction)


def find_lowest_child(snailfish_number, in_direction):
    """Find the lowest child node reached by travelling down the given direction."""
    if is_leaf(getattr(snailfish_number, in_direction)):
        return snailfish_number
    return find_lowest_child(getattr(snailfish_number, in_direction), in_direction)


def adjacent_regular_number(snailfish_number, direction):
    """Get the parent of the regular number adjacent to this snailfish_number in the given direction."""
    lowest_common_ancestor = lowest_ancestor_from(snailfish_number, INVERT[direction])
    if not lowest_common_ancestor or lowest_common_ancestor is snailfish_number:
        return None, None
    if is_leaf(getattr(lowest_common_ancestor, direction)):
        return lowest_common_ancestor, direction
    return (
        find_lowest_child(getattr(lowest_common_ancestor, direction), INVERT[direction]), 
        INVERT[direction])


def explode(snailfish_number):
    """Explode the given snailfish number."""
    left_regular_number_parent, child = adjacent_regular_number(snailfish_number, "left")
    if left_regular_number_parent:
        setattr(left_regular_number_parent, child, getattr(left_regular_number_parent, child) + snailfish_number.left)
    right_regular_number_parent, child = adjacent_regular_number(snailfish_number, "right")
    if right_regular_number_parent:
        setattr(right_regular_number_parent, child, getattr(right_regular_number_parent, child) + snailfish_number.right)
    if snailfish_number is snailfish_number.parent.left:
        snailfish_number.parent.left = 0
    else:
        snailfish_number.parent.right = 0


def split(snailfish_number, child):
    """Split the given child of the snailfish number."""
    new_child = SnailfishNumber(
        left=floor(getattr(snailfish_number, child)/2), 
        right=ceil(getattr(snailfish_number, child)/2), 
        parent=snailfish_number)
    setattr(snailfish_number, child, new_child)


def reduce(snailfish_number):
    """Reduce a snailfish number."""
    fully_reduced = False
    while not fully_reduced:
        nested_pair, _ = leftmost_exploding_pair(snailfish_number)
        if nested_pair:
            explode(nested_pair)
            continue
        parent, child = leftmost_splitting_number(snailfish_number)
        if parent:
            split(parent, child)
            continue
        fully_reduced = True
    return snailfish_number


def test_explode_lists(lists, expected):
    """Test that exploding a snailfish number defined by the given lists matches expected."""
    snailfish_number = SnailfishNumber.make(lists)
    pair, _ = leftmost_exploding_pair(snailfish_number)
    explode(pair)
    if snailfish_number.unmake() == expected:
        print("TEST PASSED")
    else:
        print("TEST FAILED")


def test_explode():
    """Test the explode() operation."""
    print("EXPLODING TESTS ...")
    test_explode_lists([[[[[9,8],1],2],3],4], expected=[[[[0,9],2],3],4])
    test_explode_lists([7,[6,[5,[4,[3,2]]]]], expected=[7,[6,[5,[7,0]]]])
    test_explode_lists([[6,[5,[4,[3,2]]]],1], expected=[[6,[5,[7,0]]],3])
    test_explode_lists([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]], expected=[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]])
    test_explode_lists([[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]], expected=[[3,[2,[8,0]]],[9,[5,[7,0]]]])


def test_split():
    """Test the split() operation."""
    print("SPLITTING TESTS ...")
    snailfish_number = SnailfishNumber.make([11, 1])
    parent, child = leftmost_splitting_number(snailfish_number)
    split(parent, child)
    if parent.unmake() == [[5,6], 1]:
        print("TEST PASSED")
    else:
        print("TEST FAILED")


def add(a, b):
    """Add two snailfish numbers."""
    a_plus_b = SnailfishNumber(a, b, None)
    a.parent = a_plus_b
    b.parent = a_plus_b
    return reduce(a_plus_b)


def magnitude(snailfish_number):
    if is_leaf(snailfish_number):
        return snailfish_number
    return 3 * magnitude(snailfish_number.left) + 2 * magnitude(snailfish_number.right)


def main():
    """Advent of Code day 18."""
    number_lists = [eval(line.rstrip()) for line in sys.stdin.readlines()]
    # Part 1.
    total_sum = SnailfishNumber.make(number_lists[0])
    for number_list in number_lists[1:]:
        total_sum = add(total_sum, SnailfishNumber.make(number_list))
    print(magnitude(total_sum))
    # Part 2.
    largest_pair_magnitude = 0
    for i, x_list in enumerate(number_lists):
        for j, y_list in enumerate(number_lists):
            if i != j:
                x_plus_y_mag = magnitude(add(SnailfishNumber.make(x_list), SnailfishNumber.make(y_list))) 
                largest_pair_magnitude = max(x_plus_y_mag, largest_pair_magnitude)
                y_plus_x_mag = magnitude(add(SnailfishNumber.make(x_list), SnailfishNumber.make(y_list)))
                largest_pair_magnitude = max(y_plus_x_mag, largest_pair_magnitude)
    print(largest_pair_magnitude)


main()