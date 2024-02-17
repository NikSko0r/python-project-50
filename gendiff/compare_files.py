import json
import yaml
import os
from gendiff.formaters.plain import plain
from gendiff.formaters.stylish import stylish


def is_key(key, dic):
    return key in dic


def is_dic(dic):
    return type(dic) is dict


def get_path_to_file(file_):
    return os.path.abspath(file_)


def get_format_file(file_):
    return os.path.splitext(file_)[1]


def get_data_from_file(file_):
    lst_format = ['.yaml', '.yml']
    format_ = get_format_file(file_)
    path = get_path_to_file(file_)
    with open(path, encoding='utf-8') as f:
        if format_ in lst_format:
            dic = yaml.full_load(f)
        else:
            dic = json.load(f)
    return dic


def get_diff_files(dic1, dic2):
    answer = []
    keys = {**dic1, **dic2}
    for key in sorted(keys):
        if not is_key(key, dic2):
            result = {'key': key, 'status': 'removed', 'value': dic1[key]}

        elif not is_key(key, dic1):
            result = {'key': key, 'status': 'added', 'value': dic2[key]}

        elif is_dic(dic1[key]) and is_dic(dic2[key]):
            result = {'key': key, 'status': 'nested', 'value': get_diff_files(dic1[key], dic2[key])}

        elif dic1[key] == dic2[key]:
            result = {'key': key, 'status': 'same', 'value': dic1[key]}

        else:
            result = {
                'key': key, 'status': 'changed', 'old_value': dic1[key], 'new_value': dic2[key]}

        answer.append(result)
    return answer


def get_generate_diff(file1, file2, style='stylish'):
    dic1, dic2 = get_data_from_file(file1), get_data_from_file(file2)
    rows = get_diff_files(dic1, dic2)
    if style == 'stylish':
        string = stylish(rows)
    elif style == 'plain':
        string = plain(rows)
    print(string)
    return string


__all__ = (
    'get_generate_diff',
)
