import random

# Constants
BOARD_SIZE = 10
USER = 0
COMPUTER = 1
BOARD_INDEX_MIN = 0
BOARD_INDEX_MAX = BOARD_SIZE - 1

# Battleships
MAX_SIZE = 4
VERTICAL_BATTLESHIP = 'v'
HORIZONTAL_BATTLESHIP = 'h'
# A mapping from a ship size to the number of battleship of this size
# that need to be placed.
SHIP_SIZE_TO_COUNT = [0, 4, 3, 2, 1]

# Board marks
BATTLESHIP_MARK = '*'
MISS_MARK = 'X'
HIT_MARK = 'V'
EMPTY_MARK = ' '

# Numbers
# *** Those numbers are used several times for calculations, but don't have
#     a meaning besides those calculations, so they don't require a
#     separate name.
ONE = 1
TWO = 2
ZERO = 0


def main():
    print_welcome_message()
    get_and_set_seed()
    user_board, computer_board = get_boards()


def print_welcome_message():
    print('Welcome to Battleship!')


def get_and_set_seed():
    print('Please enter seed:')
    seed = int(input())
    random.seed(seed)


def get_boards():
    user_board = get_user_board()
    computer_board = get_computer_board()

    return user_board, computer_board


def generate_empty_board(size):
    return [[EMPTY_MARK for _ in range(size)] for _ in range(size)]


def is_battleship_in_range(row, column, size, alignment):
    start_in_range = is_indexes_in_range(row, column)

    # Assume the alignment is vertical
    end_row = calculate_new_battleship_end(row, size)
    end_column = column

    # Check if the alignment is horizontal
    if alignment == HORIZONTAL_BATTLESHIP:
        end_row = row
        end_column = calculate_new_battleship_end(column, size)

    end_in_range = is_indexes_in_range(end_row, end_column)

    return start_in_range and end_in_range


def is_indexes_near_battleship(row, column, board):
    outer_range = get_iteration_range(row)
    inner_range = get_iteration_range(column)

    for i in outer_range:
        for j in inner_range:
            if board[i][j] == BATTLESHIP_MARK:
                return True

    return False


def get_iteration_range(number):
    return range(max(number - ONE, 0), min(number + TWO, BOARD_SIZE))


def calculate_new_battleship_end(index, size):
    return index + size - ONE


def is_indexes_in_range(row, column):
    return is_value_in_range(row) and is_value_in_range(column)


def is_value_in_range(number):
    return number >= BOARD_INDEX_MIN and number <= BOARD_INDEX_MAX


if __name__ == '__main__':
    main()
