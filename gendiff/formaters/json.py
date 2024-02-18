import json


def to_json(dicts):
    result = {}

    for dic in dicts:
        key = dic["key"]
        status = dic["status"]
        current_value = dic.get("value")

        if status == "added":
            result |= {key: {"status": status, "new_value": get_value(current_value)}}

        elif status == "removed":
            result |= {key: {"status": status, "old_value": get_value(current_value)}}

        elif status == "changed":
            result |= {
                key: {
                    "status": status,
                    "old_value": get_value(dic["old_value"]),
                    "new_value": get_value(dic["new_value"]),
                }
            }

        elif status == "same" or status == "nested":
            result |= {key: get_value(current_value)}
    return result


def get_value(value):
    if isinstance(value, list):
        return to_json(value)
    return value


def generate_json(dicts):
    string = json.dumps(to_json(dicts), indent=2)
    return string
