import sys


def parse_commands(command_strings):
    """Parse a list of command strings."""
    for string in command_strings:
        direction, value = string.split()
        yield direction, int(value)


def follow_commands_1(commands):
    """Follow commands for part 1."""
    horizontal, depth = 0, 0
    for direction, value in commands:
        if direction == "forward":
            horizontal += value 
        elif direction == "up":
            depth -= value
        elif direction == "down":
            depth += value
    return horizontal, depth


def follow_commands_2(commands):
    """Follow commands for part 2."""
    horizontal, depth, aim = 0, 0, 0
    for direction, value in commands:
        if direction == "forward":
            horizontal += value
            depth += aim * value
        elif direction == "up":
            aim -= value
        elif direction == "down":
            aim += value
    return horizontal, depth


def part1(commands):
    horizontal, depth = follow_commands_1(commands)
    print(horizontal * depth)


def part2(commands):
    horizontal, depth = follow_commands_2(commands)
    print(horizontal * depth)


if __name__ == "__main__":
    commands = list(parse_commands(sys.stdin.readlines()))
    part1(commands)
    part2(commands)