def to_plain(answer):

    def inner(answer, path=''):
        rows = []

        for value in answer:
            key = value['key']
            new_path = path
            new_path += f'{key}.'
            new_value = get_value(value.get('value'))

            if value['status'] == 'removed':
                line = f"Property '{path}{key}' was removed"
                rows.append(line)

            elif value['status'] == 'added':
                line = f"Property '{path}{key}' was added with value: {new_value}"
                rows.append(line)

            elif value['status'] == 'nested' or value['status'] == 'same':
                if isinstance(value['value'], list):
                    line = inner(value['value'], new_path)
                    rows.append(line)

            else:
                old_value = get_value(value.get('old_value'))
                new_value = get_value(value.get('new_value'))
                line = f"Property '{path}{key}' was updated. From {old_value} to {new_value}"
                rows.append(line)
        return '\n'.join(rows)
    return inner(answer, '')


def get_value(value):
    if isinstance(value, dict):
        return "[complex value]"

    elif isinstance(value, bool):
        return 'true' if value else 'false'

    elif value is None:
        return 'null'

    elif isinstance(value, int):
        return value

    return f"'{value}'"
