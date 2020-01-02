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

# Messages codes to print with the board
CURRENT_BOARD_CODE = 0
USER_FOLLOWING_TABLE_CODE = 1
COMPUTER_FOLLOWING_TABLE_CODE = 2

# Numbers
# *** Those numbers are used several times for calculations, but don't have
#     a meaning besides those calculations, so they don't require a
#     separate name.
ONE = 1
TWO = 2
ZERO = 0


def main():
    """
    Plays the game, from start to finish.
    """
    print_welcome_message()
    get_and_set_seed()
    user_board, computer_board = get_boards()
    print_battleships_located()
    winner = play_game(user_board, computer_board)
    print_winner_message(winner)


def print_welcome_message():
    """
    Prints a welcome message.
    """
    print('Welcome to Battleship!')


def get_and_set_seed():
    """
    Gets the seed from the user, and sets it in the random class.
    """
    print('Please enter seed:')
    seed = int(input())
    random.seed(seed)


def get_boards():
    """
    Gets the boards from the user and the computer.

    :return: The boards of the user and the computer, filled with
             battleships
    :rtype: tuple[list[list[str]], list[list[str]]]
    """
    user_board = get_board(USER)
    computer_board = get_board(COMPUTER)

    return user_board, computer_board


def get_board(player):
    """
    Gets the board from a given player.

    :param player: The player
    :type player: int

    :return: The board of that user, filled with battleships
    :rtype: list[list[str]]
    """
    board = generate_empty_board(BOARD_SIZE)

    # Iterate on every battleship size
    for battleship_size in range(len(SHIP_SIZE_TO_COUNT)):
        for battleship in range(SHIP_SIZE_TO_COUNT[battleship_size]):
            row, column, alignment = get_valid_battleship(player,
                                                          battleship_size,
                                                          board)
            battleship_indexes = get_battleship_indexes(row, column,
                                                        battleship_size,
                                                        alignment)
            # Set the battleship marks
            for current_row, current_column in battleship_indexes:
                set_board_by_index(current_row, current_column,
                                   BATTLESHIP_MARK, board)

    return board


def get_valid_battleship(player, size, board):
    """
    Gets a valid battleship location and alignment from a given player
    in a given size.

    :param player: The player
    :type player: int
    :param size: The size of the battleship
    :type size: int
    :param board: The board of the user
    :type board: list[list[str]]

    :return: The location and alignment of the battleship
    :rtype: tuple[int, int, str]
    """
    valid_battleship = False
    first_try = True
    while not valid_battleship:
        if player == USER:
            if first_try:
                print_board_with_message(board, CURRENT_BOARD_CODE)
            row, column, alignment = get_battleship_from_user(size,
                                                              first_try)
            first_try = False
        else:
            row, column, alignment = get_battleship_from_computer()
        if is_battleship_valid(row, column, size, alignment, board):
            valid_battleship = True

    return row, column, alignment


def get_battleship_from_user(size, is_first_try):
    """
    Gets a battleship location and alignment from the user.

    *** The location and the alignment might be invalid.

    :param size: The size of the battleship
    :type size: int
    :param is_first_try: Is this the first attempt to get the battleship's
                         information
    :type is_first_try: bool

    :return: The location and alignment of the battleship
    :rtype: tuple[int, int, str]

    """
    # Assume it's not the first try
    message = f"ERROR: Invalid location\nPlease enter location for " \
              f"Battleship of size {size} again:"

    # Check if it's the first try
    if is_first_try:
        message = f"Enter location for Battleship of size {size}:"

    print(message)
    user_input = input()
    indexes, alignment = user_input.split(' ')
    row, column = get_indexes_from_string(indexes)

    return row, column, alignment


def get_indexes_from_string(str_indexes):
    """
    Gets the row and the column out of a string in the format column,row.

    :param str_indexes: The string
    :type str_indexes: str

    :return: The row and the column that extracted from the string
    :rtype: tuple[int, int]
    """
    separated_indexes = str_indexes.split(',')
    separated_indexes = [int(index) for index in separated_indexes]
    column, row = separated_indexes
    return row, column


def get_battleship_from_computer():
    """
    Gets a battleship location and alignment from the computer.

    *** The location and the alignment might be invalid.

    :return: The location and alignment of the battleship
    :rtype: tuple[int, int, str]
    """
    row, column = get_random_indexes()
    alignments = [HORIZONTAL_BATTLESHIP, VERTICAL_BATTLESHIP]
    alignment_index = random.randint(ZERO, ONE)
    alignment = alignments[alignment_index]
    return row, column, alignment


def get_random_indexes():
    """
    Gets random row and column.

    :return: The row and column
    :rtype: tuple[int, int]
    """
    column = get_random_index()
    row = get_random_index()
    return row, column


def get_random_index():
    """
    Gets a random index, within the boundaries of the board.

    :return: The index
    :rtype: int
    """
    return random.randint(BOARD_INDEX_MIN, BOARD_INDEX_MAX)


def is_battleship_valid(row, column, size, alignment, board):
    """
    Checks if a battleship of a given size can  in the given row
    and column and in the given alignment.

    :param row: The row of the board
    :type row: int
    :param column: The column of the board
    :type column: int
    :param size: The size of the battleship
    :type size: int
    :param alignment: The alignment of the battleship
    :type alignment: str
    :param board: The board of one of the players
    :type board: list[list[str]]

    :return: Whether or the the battleship can be located
    :rtype: bool
    """
    if is_battleship_in_range(row, column, size, alignment):
        if not is_battleship_near_battleships(row, column, size, alignment,
                                              board):
            return True
    return False


def generate_empty_board(size):
    """
    Generates an empty board in a given size.

    :param size: The size of the board
    :type size: int

    :return: An empty board
    :rtype: list[list[str]]
    """
    return [[EMPTY_MARK for _ in range(size)] for _ in range(size)]


def is_battleship_in_range(row, column, size, alignment):
    """
    Checks if the battleship can be located in the board without exceeding
    the boundaries.

    :param row: The row of the battleship
    :type row: int
    :param column: The column of the battleship
    :type column: int
    :param size: The size of the battleship
    :type size: int
    :param alignment: The alignment of the battleship
    :type alignment: str

    :return: Whether or not the battleship is within the board's
             boundaries.
    :rtype: bool
    """
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
    """
    Checks if a given battleship is near other battleships, that already
    have been located on the board.

    :param row: The row of the battleship
    :type row: int
    :param column: The column of the battleship
    :type column: int
    :param size: The size of the battleship
    :type size: int
    :param alignment: The alignment of the battleship
    :type alignment: str
    :param board: The board of one of the players
    :type board: list[list[str]]

    :return: Whether or not the battleship is near other battleships
    :rtype: bool
    """
    battleship_indexes = get_battleship_indexes(row, column, size,
                                                alignment)
    for current_row, current_column in battleship_indexes:
        if is_indexes_near_battleships(current_row, current_column, board):
            return True

    return False


def get_battleship_indexes(row, column, size, alignment):
    """
    Gets all of the indexes of a battleship, base on it's start index and
    alignment.

    :param row: The row of the battleship
    :type row: int
    :param column: The column of the battleship
    :type column: int
    :param size: The size of the battleship
    :type size: int
    :param alignment: The alignment of the battleship
    :type alignment: str

    :return: All of the indexes of a battleship
    :rtype: list[list[int]]
    """
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
    """
    Checks if the given indexes are near some battleship in the board.

    :param row: The row of the board
    :type row: int
    :param column: The column of the board
    :type column: int
    :param board: The board of one of the players
    :type board: list[list[str]]

    :return: Whether or not those indexes near some battleship
    :rtype: bool
    """
    outer_range = get_iteration_range(row)
    inner_range = get_iteration_range(column)

    for i in outer_range:
        for j in inner_range:
            if board[i][j] == BATTLESHIP_MARK:
                return True

    return False


def set_board_after_attack(row, column, board):
    """
    Sets the board after the attack, based on whether it's a hit or a miss.

    :param row: The row of the board
    :type row: int
    :param column: The column of the board
    :type column: int
    :param board: The board of one of the players
    :type board: list[list[str]]
    """
    new_value = MISS_MARK  # Assume it's a miss

    if board[row][column] == BATTLESHIP_MARK:  # Check if it's a hit
        new_value = HIT_MARK

    set_board_by_index(row, column, new_value, board)


def set_board_by_index(row, column, new_value, board):
    """
    Sets the the value in a certain place in the board, into a given
    new value.

    :param row: The row of the board
    :type row: int
    :param column: The column of the board
    :type column: int
    :param new_value: The new value
    :type new_value: str
    :param board: The board of one of the players
    :type board: list[list[str]]
    """
    board[row][column] = new_value


def get_iteration_range(number):
    """
    Gets the iteration range for the battleship location validity check.

    # TODO: better documentation!!!
    :param number: The number
    :type number: int

    :return: The iteration range for the battleship location validity check
    :rtype: range
    """
    return range(max(number - ONE, ZERO), min(number + TWO, BOARD_SIZE))


def calculate_new_battleship_end(index, size):
    """
    Calculates the end of the battleship, and returns it.

    *** The meaning of the end of the battleship is determined by its
        alignment:
                  - Vertical: The bottom indexes
                  - Horizontal: The right indexes

    :param index: The start of the battleship
    :type index: int
    :param size: The size of the battleship
    :type size: int

    :return: The end of the battleship
    :rtype: int
    """
    return index + size - ONE


def is_indexes_in_range(row, column):
    """
    Checks if both the row and the column are within the boundaries of
    the board.

    :param row: The row
    :type row: int
    :param column: The column
    :type column: int

    :return: Whether or not both of them are within the boundaries
    :rtype: bool
    """
    return is_value_in_range(row) and is_value_in_range(column)


def is_value_in_range(number):
    """
    Checks if the given number is  within the boundaries of the board.

    :param number: The number
    :type number: int

    :return: Whether or not the number is within the boundaries
    :rtype: bool
    """
    return BOARD_INDEX_MIN <= number <= BOARD_INDEX_MAX


def get_total_number_of_battleships():
    """
    Gets the total amount of battleship each player has.

    :return: The total amount of battleship of each player
    :rtype: int
    """
    return sum(SHIP_SIZE_TO_COUNT)


def play_game(user_board, computer_board):
    """
    Plays the game itself (after the boards are filled with battleships).

    :param user_board: The board of the user
    :type user_board: list[list[str]]
    :param computer_board: The board of the computer
    :type computer_board: list[list[str]]

    :return: The winner of the game
    :rtype: int
    """
    total_battleships = get_total_number_of_battleships()
    user_battleships = computer_battleships = total_battleships

    # Iterate as long as nobody lost
    while user_battleships > ZERO and computer_battleships > ZERO:
        computer_battleships = user_turn(computer_battleships,
                                         total_battleships, user_board,
                                         computer_board)
        # The user won
        if computer_battleships == ZERO:
            return USER

        user_battleships = computer_turn(user_battleships,
                                         total_battleships, user_board)

    # The computer won
    return COMPUTER


def user_turn(computer_battleships, total_battleships, user_board,
              computer_board):
    """
    Plays one turn of the user.

    :param computer_battleships: The current number of the computer's
                                 battleships
    :type computer_battleships: int
    :param total_battleships: The total amount of battleship each player
                              has.
    :type total_battleships: int
    :param user_board: The board of the user
    :type user_board: list[list[str]]
    :param computer_board: The board of the computer
    :type computer_board: list[list[str]]

    :return: The new number of the computer's battleships
    :rtype: int
    """
    # Print the boards and the messages
    print_board_with_message(computer_board, USER_FOLLOWING_TABLE_CODE)
    print_board_with_message(user_board, COMPUTER_FOLLOWING_TABLE_CODE)
    print("It's your turn!")

    # Get the attack
    row, column = get_valid_attack(USER, computer_board)

    # Set the board after the attack
    set_board_after_attack(row, column, computer_board)

    new_battleships = count_battleships(computer_board)

    # The computer's battleship has been drowned
    if new_battleships != computer_battleships:
        print_drown_battleship(COMPUTER, new_battleships,
                               total_battleships)

    return new_battleships


def computer_turn(user_battleships, total_battleships, user_board):
    """
    Plays one turn of the computer.

    :param user_battleships: The current number of the user's
                                 battleships
    :type user_battleships: int
    :param total_battleships: The total amount of battleship each player
                              has.
    :type total_battleships: int
    :param user_board: The board of the user
    :type user_board: list[list[str]]

    :return: The new number of the user's battleships
    :rtype: int
    """
    # Get the attack
    row, column = get_valid_attack(COMPUTER, user_board)

    # Set the board after the attack
    set_board_after_attack(row, column, user_board)

    new_battleships = count_battleships(user_board)

    # The user's battleship has been drowned
    if new_battleships != user_battleships:
        print_drown_battleship(USER, new_battleships,
                               total_battleships)

    return new_battleships


def get_valid_attack(player, board):
    """
    Gets a valid attack indexes from a given player

    :param player: The player
    :type player: int
    :param board: The following table of the player
    :type board: list[list[str]]

    :return: Valid row and column to attack
    :rtype: tuple[int, int]
    """
    valid_attack = False
    is_first_try = True
    while not valid_attack:
        if player == USER:
            row, column = get_attack_from_user(is_first_try)
            is_first_try = False
        else:
            row, column = get_random_indexes()

        if is_attack_valid(row, column, board):
            valid_attack = True

    return row, column


def is_attack_valid(row, column, board):
    """
    Checks if it's valid to attack in the given row and column.

    :param row: The row
    :type row: int
    :param column: The column
    :type column: int
    :param board: The following table of one of the players
    :type board: list[list[str]]

    :return: Whether or not the attack is valid
    :rtype: bool
    """
    if is_indexes_in_range(row, column):
        # Check if the player didn't already attack in this row and column
        if board[row][column] not in [HIT_MARK, MISS_MARK]:
            return True

    return False


def get_attack_from_user(is_first_try):
    """
    Gets from the user row and column to attack.

    *** The row and the column might be invalid.

    :param is_first_try: Is this the first attempt to get the attack's
                         information
    :type is_first_try: bool

    :return: Row and column to attack
    :rtype: tuple[int, int]
    """
    # Assume it's not the first try
    message = "Error: Invalid attack...\nPlease try again:"

    # Check if it's the first try
    if is_first_try:
        message = "Enter location for attack:"

    print(message)
    indexes = input()
    row, column = get_indexes_from_string(indexes)

    return row, column


def check_if_top_vertical(row, column, board):
    """
    Checks if board[column][row] is the top vertical part of the
    battleship.

    :param row: The row
    :type row: int
    :param column: The column
    :type column: int
    :param board: The following table of one of the players
    :type board: list[list[str]]

    :return: Whether ot not the location is top vertical
    :rtype: bool
    """
    for j in range(column - ONE, max(column - MAX_SIZE, -ONE), -ONE):
        if board[row][j] not in [BATTLESHIP_MARK, HIT_MARK]:
            return True
        if board[row][j] == BATTLESHIP_MARK:
            return False

    return True


def check_if_top_horizontal(row, column, board):
    """
    Checks if board[column][row] is the top horizontal part of the
    battleship.

    :param row: The row
    :type row: int
    :param column: The column
    :type column: int
    :param board: The following table of one of the players
    :type board: list[list[str]]

    :return: Whether ot not the location is top horizontal
    :rtype: bool
    """
    for i in range(row - ONE, max(row - MAX_SIZE, -ONE), -ONE):
        if board[i][column] not in [BATTLESHIP_MARK, HIT_MARK]:
            return True
        if board[i][column] == BATTLESHIP_MARK:
            return False

    return True


def count_battleships(board):
    """
    Counts the number of battleships left on the table.
    :param board: a following table
    :return: The number of battleships.
    """
    counter = ZERO
    num_rows = num_cols = BOARD_SIZE
    for i in range(num_rows):
        for j in range(num_cols):
            if board[i][j] != BATTLESHIP_MARK:
                continue
            if check_if_top_horizontal(i, j, board) \
                    and check_if_top_vertical(i, j, board):
                counter += ONE
    return counter


def print_drown_battleship(player, battleships, total_battleships):
    """
    Prints that a battleship of a given player has been drowned.

    :param player: The player whose  battleship has been drowned
    :type player: int
    :param battleships: The number of battleships that left for the user.
    :type battleships: int
    :param total_battleships: The total amount of battleship the player
                              has.
    :type total_battleships: int
    """
    # Assume that the player is the computer
    message = "The computer's battleship has been drowned."

    # Check if the player is the user
    if player == USER:
        message = "Your battleship has been drowned."

    message += f"\n{battleships}/{total_battleships} battleships remain!"

    print(message)


def print_battleships_located():
    """
    Prints that all of the battleships have been located.
    """
    print('All battleships have been located successfully!')


def print_winner_message(player):
    """
    Prints a message when the game is over.

    :param player: The winner player
    :type player: int
    """
    if player == USER:
        print('Congrats! You are the winner :)')
    else:
        print('Game over! The computer won the fight :(')


def print_board_with_message(board, message_code):
    """
    Prints the given board, with a message.

    :param board: The board to print
    :type board: list[list[str]]
    :param message_code: The code of the message to print
    :type message_code: int
    """
    # Assume the message is about the player's current board
    message = "Your current board:"
    player = USER

    if message_code == USER_FOLLOWING_TABLE_CODE:
        message = "Your following table:"
        player = COMPUTER
    elif message_code == COMPUTER_FOLLOWING_TABLE_CODE:
        message = "The computer's following table:"

    print(message)
    print_board(board, player)


def print_board(board, player):
    """
    Prints the given board.

    :param board: The board to print
    :type board: list[list[str]]
    :param player: The player that the board
    :type player: The current player
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
