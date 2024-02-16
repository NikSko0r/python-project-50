import json
import yaml
import os
import itertools


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


def stylish(answer, replacer='    ', depth=1):

    def inner(answer, depth):
        indent = replacer * depth
        current_indent = (depth - 1) * replacer
        new_depth = depth + 1
        rows = []
        for value in answer:
            new_value = get_value(value.get('value'), new_depth)
            key = value['key']
            if value['status'] == 'removed':
                sign = '-'
                rows.append(f'{indent[:-2]}{sign} {key}: {new_value}')

            elif value['status'] == 'added':
                sign = '+'
                rows.append(f'{indent[:-2]}{sign} {key}: {new_value}')

            elif value['status'] == 'nested':
                rows.append(f'{indent}{key}: {new_value}')

            elif value['status'] == 'same':
                rows.append(f'{indent}{key}: {new_value}')

            else:
                old_value = get_value(value.get('old_value'), new_depth)
                new_value = get_value(value.get('new_value'), new_depth)
                rows.append(f'{indent[:-2]}- {key}: {old_value}')
                rows.append(f'{indent[:-2]}+ {key}: {new_value}')
        result = itertools.chain('{', rows, [current_indent + '}'])
        return '\n'.join(result)
    return inner(answer, depth)


def get_value(value, depth):
    replacer = '    '
    indent = replacer * depth
    current_indent = (depth - 1) * replacer
    new_depth = depth + 1
    rows = []
    if isinstance(value, list):
        return stylish(value, depth=depth)
    elif isinstance(value, dict):
        for key, val in value.items():
            rows.append(f'{indent}{key}: {get_value(val, new_depth)}')
        result = itertools.chain('{', rows, [current_indent + '}'])
        return '\n'.join(result)
    elif isinstance(value, bool):
        return 'true' if value else 'false'
    elif value is None:
        return 'null'
    return value


def get_generate_diff(file1, file2, style='stylish'):
    dic1, dic2 = get_data_from_file(file1), get_data_from_file(file2)
    rows = get_diff_files(dic1, dic2)
    if style == 'stylish':
        string = stylish(rows)
    print(string)
    return string


__all__ = (
    'get_value',
    'is_key',
    'is_dic',
    'stylish',
    'get_diff_files',
    'get_data_from_file',
    'get_path_to_file',
    'get_format_file'

)
