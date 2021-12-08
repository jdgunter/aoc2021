import sys


def parse_lines(lines):
    """Parse the input lines."""
    parsed_lines = []
    for line in lines:
        pattern_string, output_string = line.split("|")
        pattern = pattern_string.split()
        outputs = output_string.split()
        parsed_lines.append((pattern, outputs))
    return parsed_lines


def count_1_4_7_8(lines):
    """Count the number of instances of 1, 4, 7, or 8 in the output 
    digits of each input line."""
    unique_segment_counts = {2, 3, 4, 7}
    count = 0
    for _, output_digits in lines:
        for output_digit in output_digits:
            if len(output_digit) in unique_segment_counts:
                count += 1
    return count


def pattern_decoder(patterns):
    """Get a decoder for the given set of patterns."""
    patterns = [frozenset(signal_pattern) for signal_pattern in patterns]
    encoder = {}
    len_five_patterns = set()
    len_six_patterns = set()

    # Decode the digits with unique segment counts.
    for signal_pattern in patterns:
        if len(signal_pattern) == 2:
            encoder[1] = signal_pattern
        elif len(signal_pattern) == 3:
            encoder[7] = signal_pattern
        elif len(signal_pattern) == 4:
            encoder[4] = signal_pattern
        elif len(signal_pattern) == 7:
            encoder[8] = signal_pattern
        elif len(signal_pattern) == 5:
            len_five_patterns.add(signal_pattern)
        elif len(signal_pattern) == 6:
            len_six_patterns.add(signal_pattern)
    
    # Decode the five-length segments.
    for signal_pattern in len_five_patterns:
        if len(signal_pattern & encoder[4]) == 2:
            encoder[2] = signal_pattern
        elif signal_pattern & encoder[7] == encoder[7]:
            encoder[3] = signal_pattern
    len_five_patterns.remove(encoder[2])
    len_five_patterns.remove(encoder[3])
    encoder[5] = min(len_five_patterns)

    # Decode the six-length segments.
    encoder[9] = encoder[5] | encoder[1]
    len_six_patterns.remove(encoder[9])
    for signal_pattern in len_six_patterns:
        if signal_pattern & encoder[7] != encoder[7]:
            encoder[6] = signal_pattern
            break
    len_six_patterns.remove(encoder[6])
    encoder[0] = min(len_six_patterns)

    return {segments: digit for digit, segments in encoder.items()}


def convert_digits_to_int(digits):
    """Convert a list of digits into a single integer."""
    return int("".join([str(digit) for digit in digits]))


def decode_output_values(lines):
    """Decode the output values in the given set of input lines."""
    decoded_outputs = []
    for patterns, output_digits in lines:
        output_digits = [frozenset(digits) for digits in output_digits]
        decoder = pattern_decoder(patterns)
        decoded_output = convert_digits_to_int(decoder[pattern] for pattern in output_digits)
        decoded_outputs.append(decoded_output)
    return decoded_outputs


def main():
    """Advent of Code day 8."""
    lines = parse_lines(sys.stdin.readlines())
    print(count_1_4_7_8(lines))
    print(sum(decode_output_values(lines)))


main()