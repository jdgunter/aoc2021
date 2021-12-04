import sys


class BingoBoard:

    def __init__(self, board):
        """Initialize a Bingo board."""
        self.board = board
        self.marked = [[False for _ in row] for row in board]
        self.dirty = False
        self.won = False

    def mark(self, num):
        """Mark off the given number if it is present on the board."""
        for row_index, row in enumerate(self.board):
            for col_index, val in enumerate(row):
                if val == num:
                    self.marked[row_index][col_index] = True
                    self.dirty = True
                    return
    
    def has_won(self):
        """Returns True if this board has won."""
        if not self.dirty:
            return self.won
        for row in self.marked:
            if all(row):
                self.won = True
                self.dirty = False
                return self.won
        transposed = zip(*self.marked)
        for col in transposed:
            if all(col):
                self.won = True
                self.dirty = False
                return self.won
        self.dirty = False
        return False
    
    def sum_unmarked_numbers(self):
        """Get the sum of unmarked numbers on the board."""
        total = 0
        for row_index, row in enumerate(self.marked):
            for col_index, marked in enumerate(row):
                if not marked:
                    total += self.board[row_index][col_index]
        return total


def parse_numbers_and_boards(input_lines):
    """Parse puzzle input."""
    numbers = [int(num_string) for num_string in input_lines[0].split(",")]
    bingo_boards = []
    for start_index in range(1, len(input_lines), 6):
        board_lines = input_lines[start_index+1:start_index+6]
        board = [[int(num_string) for num_string in line.split()] for line in board_lines]
        bingo_boards.append(BingoBoard(board))
    return numbers, bingo_boards


def part1(drawn_numbers, bingo_boards):
    """Part 1 of day 4."""
    for number in drawn_numbers:
        for board in bingo_boards:
            board.mark(number)
            if board.has_won():
                print(board.sum_unmarked_numbers() * number)
                return


def part2(drawn_numbers, bingo_boards):
    """Part 2 of day 4."""
    for number in drawn_numbers:
        winning_indices = []
        for index, board in enumerate(bingo_boards):
            board.mark(number)
            if board.has_won():
                if len(bingo_boards) == 1:
                    print(board.sum_unmarked_numbers() * number)
                    return
                winning_indices.append(index)
        for index in reversed(winning_indices):
            del bingo_boards[index]


def main():
    drawn_numbers, bingo_boards = parse_numbers_and_boards(sys.stdin.readlines())
    part1(drawn_numbers, bingo_boards)
    part2(drawn_numbers, bingo_boards)


main()