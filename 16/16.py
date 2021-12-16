import numpy as np
import sys
from dataclasses import dataclass
from math import prod
from typing import Any, List, Union

# type IDs
SUM = 0
PRODUCT = 1
MINIMUM = 2
MAXIMUM = 3
LITERAL_VALUE = 4
GREATER_THAN = 5
LESS_THAN = 6
EQUAL_TO = 7


@dataclass
class Packet:
    version: int
    type_id: int
    contents: Union[int, List["Packet"]]


def decode(hex_string):
    """Decode an array of bits from a hex string."""
    bin_string = f"{int(hex_string, 16):0>{len(hex_string)*4}b}"
    return np.array([int(bit) for bit in bin_string])


def bin_to_int(bits):
    """Convert a list of bits to an integer."""
    return sum(bit * 2 ** i for i, bit in enumerate(reversed(bits)))


def parse_value(binary_code):
    """Parse a value from the given binary code."""
    window_start_index = 0
    bits = []
    more_data = True
    while more_data:
        window = binary_code[window_start_index:window_start_index+5]
        more_data = window[0]
        bits.extend(window[1:])
        window_start_index += 5
    unparsed_code = binary_code[window_start_index:]
    return bin_to_int(bits), unparsed_code


def parse_operator(binary_code):
    """Parse an operator from the given binary code."""
    length_type_id = binary_code[0]
    subpackets = []
    if length_type_id:
        number_of_subpackets = bin_to_int(binary_code[1:12])
        other_binary_code = binary_code[12:]
        for _ in range(number_of_subpackets):
            packet, other_binary_code = parse_packet(other_binary_code)
            subpackets.append(packet)
        unparsed_code = other_binary_code
    else:
        number_of_subpacket_bits = bin_to_int(binary_code[1:16])
        other_binary_code = binary_code[16:16+number_of_subpacket_bits]
        while len(other_binary_code):
            packet, other_binary_code = parse_packet(other_binary_code)
            subpackets.append(packet)
        unparsed_code = binary_code[16+number_of_subpacket_bits:]
    return subpackets, unparsed_code


def parse_packet(binary_code):
    """Parse a packet from the given binary code."""
    version = bin_to_int(binary_code[0:3])
    type_id = bin_to_int(binary_code[3:6])
    if type_id == LITERAL_VALUE:
        value, other_binary_code = parse_value(binary_code[6:])
        return Packet(version, type_id, value), other_binary_code
    else:
        operator, other_binary_code = parse_operator(binary_code[6:])
        return Packet(version, type_id, operator), other_binary_code


def compute_version_sum(packet):
    """Compute the sum of the packet versions."""
    if packet.type_id == LITERAL_VALUE:
        return packet.version
    return packet.version + sum(compute_version_sum(subpacket) for subpacket in packet.contents) 


def evaluate(packet):
    """Evaluate the expression represented by a packet."""
    if packet.type_id == LITERAL_VALUE:
        return packet.contents
    subpackets = packet.contents
    apply_to_subpackets = lambda func: func(evaluate(subpacket) for subpacket in subpackets)
    if packet.type_id == SUM:
        return apply_to_subpackets(sum) 
    if packet.type_id == PRODUCT:
        return apply_to_subpackets(prod)
    if packet.type_id == MINIMUM:
        return apply_to_subpackets(min)
    if packet.type_id == MAXIMUM:
        return apply_to_subpackets(max)
    assert len(subpackets) == 2
    if packet.type_id == GREATER_THAN:
        return int(evaluate(subpackets[0]) > evaluate(subpackets[1]))
    if packet.type_id == LESS_THAN:
        return int(evaluate(subpackets[0]) < evaluate(subpackets[1]))
    if packet.type_id == EQUAL_TO:
        return int(evaluate(subpackets[0]) == evaluate(subpackets[1]))
    raise ValueError(f"Unexpected packet type ID: {packet.type_id}")


def main():
    """Advent of Code day 16."""
    binary_code = decode(sys.stdin.read().rstrip())
    root_packet, _ = parse_packet(binary_code)
    print(compute_version_sum(root_packet))
    print(evaluate(root_packet))


main()