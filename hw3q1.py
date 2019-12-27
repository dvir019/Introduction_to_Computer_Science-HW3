import random

def main():
    print_welcome_message()
    get_and_set_seed()

def print_welcome_message():
    print('Welcome to Battleship!')

def get_and_set_seed():
    print('Please enter seed:')
    seed = int(input())
    random.seed(seed)


if __name__ == '__main__':
    main()