import random

# Constants
N = 10
USER = 0
COMPUTER = 1

# Battleships
MAX_SIZE = 4
# A mapping from a ship size to the number of battleship of this size
# that need to be placed.
SHIP_SIZE_TO_COUNT = [0, 4, 3, 2, 1]

# Board marks
BATTLESHIP_MARK = '*'
MISS_MARK = 'X'
HIT_MARK = 'V'
EMPTY_MARK = ' '


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
    return [[EMPTY_MARK for _ in range(size)]for _ in range(size)]


if __name__ == '__main__':
    main()
