"""
-----------------------------------------------------------------------------------------------------
This program helps to check the homework in python.
The program redirects the output and the input of some code,
compares between the output and the expected output, and reports about any difference between them.
-----------------------------------------------------------------------------------------------------
Author: Dvir Twito
Year  : 2019
-----------------------------------------------------------------------------------------------------
"""

# Imports
import difflib
import sys
import os

# File types
INPUT = "in"
EXPECTED_OUTPUT = "out"
MY_OUTPUT = "MyOut"
PYTHON = ""

# File extensions
PYTHON_EXTENSION = ".py"
TEXT_EXTENSION = ".txt"
FILE_DICT = {INPUT: TEXT_EXTENSION,
             EXPECTED_OUTPUT: TEXT_EXTENSION,
             MY_OUTPUT: TEXT_EXTENSION,
             PYTHON: PYTHON_EXTENSION}

# Colors
RED = "\033[1;31m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"

# Error
ERROR = "ERROR"


def main():
    args = sys.argv[1:]
    if not is_arguments_valid(args):
        print("Invalid parameters.")
        return
    homework, question, start_index, stop_index = get_numbers(args)
    for file_index in range(start_index, stop_index + 1):
        execute_file = generate_file_name(homework, question, file_index, PYTHON)
        input_file = generate_file_name(homework, question, file_index, INPUT)
        expected_output_file = generate_file_name(homework, question, file_index, EXPECTED_OUTPUT)
        my_output_file = generate_file_name(homework, question, file_index, MY_OUTPUT)

        execute_and_redirect(execute_file, input_file, my_output_file)

        files_differences = get_files_differences(expected_output_file, my_output_file)

        if files_differences == ERROR:
            break

        elif files_differences != "":
            print(f"\n{RED}{files_differences}{RESET}")
        else:
            print(f"\n{GREEN}{my_output_file} exactly matches {expected_output_file}{RESET}")


def is_arguments_valid(lst):
    """
    Checks if the command-line arguments are valid.

    :param lst: The command-line arguments, without the file name.
    :type lst: list[str]
    :return: Whether or not they are valid.
    :rtype: bool
    """
    if len(lst) != 4:
        return False
    for item in lst:
        if not item.isdigit():
            return False
    if int(lst[-1]) < int(lst[-2]):
        return False
    return True


def get_numbers(lst):
    """
    Gets a list of string that representing numbers, and return the list of the numbers.

    :param lst: List of string that representing numbers
    :type lst: list[str]
    :return: The list of the numbers
    :rtype: list[int]
    """
    return [int(num_str) for num_str in lst]


def generate_file_name(homework, question, index, file_type):
    """
    Generate the file full name according to the:
        - Homework number
        - Question number
        - The index of the the example
        - The file type

    :param homework: The homework number.
    :type homework: int
    :param question:
    :type question: int
    :param index: The index of the example
    :type index: int
    :param file_type: The type of the file
    :type file_type: str
    :return: The file full name
    :rtype: str
    """
    return f"hw{homework}q{question}{file_type}{index if file_type != PYTHON else ''}{FILE_DICT[file_type]}"


def execute_and_redirect(execute_file, input_file, output_file):
    """
    Executes the python code, and redirects its input and output.

    :param execute_file: The file to execute
    :type execute_file: str
    :param input_file: The input file
    :type input_file: str
    :param output_file: The output file
    :type output_file: str
    """
    os.system(f"python ..\\{execute_file} < {input_file} > {output_file}")


def get_files_differences(expected_output_file_name, my_output_file_name):
    """
    Get the differences between the expected output file and the redirected output file.

    :param expected_output_file_name: The name of the expected output file
    :type expected_output_file_name: str
    :param my_output_file_name: The name of the redirected output file
    :type my_output_file_name: str
    :return: The differences between the file
    :rtype: str
    """
    try:
        with open(expected_output_file_name, 'r') as expected_output_file, \
                open(my_output_file_name, 'r') as my_output_file:
            expected_output = expected_output_file.readlines()
            my_output = my_output_file.readlines()

    except FileNotFoundError:
        return ERROR

    else:
        differ = difflib.Differ()
        diffs = differ.compare(my_output, expected_output)

        diffs_string = "\n\t".join([line.strip('\n') for line in diffs if line.startswith(("+ ", "- "))])

        if diffs_string != "":
            diffs_string = f"Differences between {expected_output_file_name} and " \
                           f"{my_output_file_name}:\n\t{diffs_string}"

        return diffs_string


if __name__ == '__main__':
    main()
