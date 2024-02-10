import json
import yaml
import os


def is_key(key, dic):
    return key in dic


def get_path_to_file(_file):
    return os.path.abspath(_file)


def get_format_file(_file):
    return os.path.splitext(_file)[1]


def get_data_from_file(_file):
    lst_format = ['.yaml', '.yml']
    _format = get_format_file(_file)
    _path = get_path_to_file(_file)
    with open(_path, encoding='utf-8') as f:
        if _format in lst_format:
            dic = yaml.full_load(f)
        else:
            dic = json.load(f)
    return dic


def get_diff_between_files(file1, file2):
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


__all__ = (
    'get_diff_between_files',
    'is_key',
    'get_data_from_file',
    'get_path_to_file',
    'get_format_file'

)
