#! usr/bin/env python3

import argparse
import json


def is_key(key, dic):
    return key in dic


def get_data_from_file(file1):
    with open(file1, encoding='utf-8') as file1:
        dic = json.load(file1)
    return dic


def generate_diff(file1, file2):
    dic1, dic2 = get_data_from_file(file1), get_data_from_file(file2)
    lst = sorted({**dic1, **dic2})
    string = ''
    for i in lst:
        if is_key(i, dic1) and is_key(i, dic2):
            if dic1[i] == dic2[i]:
                string += f'    {i}: {dic1[i]}\n'
            else:
                string += f'  - {i}: {dic1[i]}\n'
                string += f'  + {i}: {dic2[i]}\n'
        else:
            if is_key(i, dic1):
                string += f'  - {i}: {dic1[i]}\n'
            else:
                string += f'  + {i}: {dic2[i]}\n'
    string = '{\n' + string + '}'
    print(string)
    return string


def gendiff():
    parser = argparse.ArgumentParser(
        description='Compares two configuration files and shows a difference.',)
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format', help='set format of output')
    args = parser.parse_args()
    generate_diff(args.first_file, args.second_file)


def main():
    gendiff()


if __name__ == '__main__':
    main()

__all__ = (
    'generate_diff',
    'gendiff',
    'is_key',
)
