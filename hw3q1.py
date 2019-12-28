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
    print_battleships_located()


def print_welcome_message():
    print('Welcome to Battleship!')


def get_and_set_seed():
    print('Please enter seed:')
    seed = int(input())
    random.seed(seed)


def get_boards():
    user_board = get_board(USER)
    computer_board = get_board(COMPUTER)

    return user_board, computer_board


def get_board(player):
    board = generate_empty_board(BOARD_SIZE)
    for battleship_size in range(len(SHIP_SIZE_TO_COUNT)):
        for battleship in range(SHIP_SIZE_TO_COUNT[battleship_size]):
            row, column, alignment = get_valid_battleship(player,
                                                          battleship_size,
                                                          board)
            battleship_indexes = get_battleship_indexes(row, column,
                                                        battleship_size,
                                                        alignment)
            for current_row, current_column in battleship_indexes:
                set_board_by_index(current_row, current_column,
                                   BATTLESHIP_MARK, board)

    return board


def get_valid_battleship(player, size, board):
    valid_battleship = False
    first_try = True
    while not valid_battleship:
        if player == USER:
            if first_try:
                print("Your current board:")
                print_board(board, USER)
            row, column, alignment = get_battleship_from_user(size,
                                                              first_try)
            first_try = False
        else:
            row, column, alignment = get_battleship_from_computer()
        if is_battleship_in_range(row, column, size, alignment):
            if not is_indexes_near_battleships(row, column, board):
                valid_battleship = True

    return row, column, alignment


def get_battleship_from_user(size, is_first_try):
    if is_first_try:
        message = f"Enter location for Battleship of size {size}:"
    else:
        message = f"ERROR: Invalid location\n" \
                  f"Please enter location for Battleship of size {size} " \
                  f"again:"

    print(message)
    user_input = input()
    indexes, alignment = user_input.split(' ')
    row, column = get_indexes_from_string(indexes)

    return row, column, alignment


def get_indexes_from_string(str_indexes):
    separated_indexes = str_indexes.split(',')
    separated_indexes = [int(index) for index in separated_indexes]
    column, row = separated_indexes
    return row, column


def get_battleship_from_computer():
    row, column = get_random_indexes()
    alignments = [HORIZONTAL_BATTLESHIP, VERTICAL_BATTLESHIP]
    alignment_index = random.randint(ZERO, ONE)
    alignment = alignments[alignment_index]

    return row, column, alignment


def get_random_indexes():
    row = get_random_index()
    column = get_random_index()

    return row, column


def get_random_index():
    return random.randint(BOARD_INDEX_MIN, BOARD_INDEX_MAX)


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


def is_battleship_near_battleships(row, column, size, alignment, board):
    battleship_indexes = get_battleship_indexes(row, column, size,
                                                alignment)
    for current_row, current_column in battleship_indexes:
        if is_indexes_near_battleships(current_row, current_column, board):
            return True

    return False


def get_battleship_indexes(row, column, size, alignment):
    indexes = []
    for i in range(size):
        # Assume the alignment is vertical
        new_indexes = [row + i, column]

        # Check if the alignment is horizontal
        if alignment == HORIZONTAL_BATTLESHIP:
            new_indexes = [row, column + i]

        indexes.append(new_indexes)

    return indexes


def is_indexes_near_battleships(row, column, board):
    outer_range = get_iteration_range(row)
    inner_range = get_iteration_range(column)

    for i in outer_range:
        for j in inner_range:
            if board[i][j] == BATTLESHIP_MARK:
                return True

    return False


def set_board_by_index(row, column, new_value, board):
    board[row][column] = new_value


def get_iteration_range(number):
    return range(max(number - ONE, 0), min(number + TWO, BOARD_SIZE))


def calculate_new_battleship_end(index, size):
    return index + size - ONE


def is_indexes_in_range(row, column):
    return is_value_in_range(row) and is_value_in_range(column)


def is_value_in_range(number):
    return number >= BOARD_INDEX_MIN and number <= BOARD_INDEX_MAX


def get_number_of_battleships():
    return sum(SHIP_SIZE_TO_COUNT)

def print_battleships_located():
    print('All battleships have been located successfully!')

def print_board(board, player):
    """
    Prints the board which corresponds to the player.
    :param board: the players board
    :param player: the current player
    :return:
    """
    print('    ', end='')
    print(' '.join([str(row) for row in range(BOARD_SIZE)]))
    print('    ', end='')
    print(' '.join(['-' for _ in range(BOARD_SIZE)]))
    for row in range(0, BOARD_SIZE, 1):
        print(row, end=' | ')
        if player == COMPUTER:
            print(' '.join(board[row]).replace('*', ' '))
        else:
            print(' '.join(board[row]))

    print()


if __name__ == '__main__':
    main()
