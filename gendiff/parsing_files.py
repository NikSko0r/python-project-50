import argparse

from gendiff.compare_files import get_diff_between_files


def parsing_files():
    parser = argparse.ArgumentParser(
        description='Compares two configuration files and shows a difference.',)
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format', help='set format of output')
    args = parser.parse_args()
    get_diff_between_files(args.first_file, args.second_file)
