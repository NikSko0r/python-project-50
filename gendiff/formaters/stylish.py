import itertools


def to_stylish(answer, replacer='    ', depth=1):

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
        return to_stylish(value, depth=depth)
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
