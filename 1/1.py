import sys


def count_increasing_sums(ls, window_size):
    num_increasing_sums = 0
    for index in range(1, len(ls)):
        current_window = ls[index:index+window_size]
        prev_window = ls[index-1:index+window_size-1]
        if sum(prev_window) < sum(current_window):
            num_increasing_sums += 1
    return num_increasing_sums


def part1(input_list):
    print(count_increasing_sums(input_list, window_size=1))


def part2(input_list):
    print(count_increasing_sums(input_list, window_size=3))


if __name__ == "__main__":
    measurements = [int(line) for line in sys.stdin.readlines()]
    part1(measurements)
    part2(measurements)

