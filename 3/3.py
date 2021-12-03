import sys


def most_and_least_common_bits(bstrings):
    """Create two new binary strings from the most and least common bits."""
    string_lengths = len(bstrings[0])
    ones_count = [0] * string_lengths
    zeroes_count = [0] * string_lengths
    for bstring in bstrings:
        for index, ch in enumerate(bstring):
            if ch == '0':
                zeroes_count[index] += 1
            elif ch == '1':
                ones_count[index] += 1
    most_common_bits = []
    least_common_bits = []
    for zero_count, one_count in zip(zeroes_count, ones_count):
        if zero_count > one_count:
            most_common_bits.append(0)
            least_common_bits.append(1)
        elif zero_count < one_count:
            most_common_bits.append(1)
            least_common_bits.append(0)
        else:
            raise ValueError("bit counts equal")
    return most_common_bits, least_common_bits


def filter_bstrings(bstrings, indices, string_index, filter_func):
    """
    Filter out strings with 0 or 1 at string_index according to the given filter_func.
    
    Returns the last string remaining after all other strings have been filtered.
    """
    # Base cases: either only one index left, or we've reached the last string index.
    if len(indices) == 1:
        return bstrings[indices[0]]
    elif string_index == len(bstrings[0]):
        assert len(indices) == 1
        return bstrings[indices[0]]

    indices_with_one = []
    indices_with_zero = []
    for index in indices:
        ch = bstrings[index][string_index]
        if ch == '0':
            indices_with_zero.append(index)
        elif ch == '1':
            indices_with_one.append(index)

    next_indices = filter_func(indices_with_zero, indices_with_one)
    return filter_bstrings(bstrings, next_indices, string_index + 1, filter_func)


def oxygen_bit_criteria(indices_with_zero, indices_with_one):
    """Bit criteria for determining the oxygen generator rating."""
    n_zeroes = len(indices_with_zero)
    n_ones = len(indices_with_one)
    if n_ones >= n_zeroes:
        return indices_with_one
    return indices_with_zero


def co2_bit_criteria(indices_with_zero, indices_with_one):
    """Bit criteria for determining the CO2 scrubber rating."""
    n_zeroes = len(indices_with_zero)
    n_ones = len(indices_with_one)
    if n_zeroes <= n_ones:
        return indices_with_zero
    return indices_with_one


def bstring_to_int(bstring):
    """
    Convert binary string to an integer.
    
    The binary string may be either a list of 0 and 1 integers or a string.
    """
    value = 0
    for index, bit in enumerate(reversed(bstring)):
        if bit == 1 or bit == '1':
            value += 2 ** index
    return value


def part1(bstrings):
    """Part 1 of AOC2021 day 3."""
    most_common_bits, least_common_bits = most_and_least_common_bits(bstrings)
    gamma = bstring_to_int(most_common_bits)
    epsilon = bstring_to_int(least_common_bits)
    print(gamma * epsilon)


def part2(bstrings):
    """Part 2 of AOC2021 day 3."""
    oxygen_bits = filter_bstrings(bstrings, range(len(bstrings)), 0, oxygen_bit_criteria)
    oxygen_rating = bstring_to_int(oxygen_bits)
    co2_bits = filter_bstrings(bstrings, range(len(bstrings)), 0, co2_bit_criteria)
    co2_rating = bstring_to_int(co2_bits)
    print(oxygen_rating * co2_rating)


if __name__ == "__main__":
    bstrings = [string[:-1] for string in sys.stdin.readlines()]
    part1(bstrings)
    part2(bstrings)