import json
import yaml
import pytest

from gendiff.compare_files import (
    is_key,
    get_diff_files,
    stylish,
    get_value,
    get_generate_diff,
    get_data_from_file,
    get_format_file,
    get_path_to_file,
)
from gendiff.formaters.plain import plain


@pytest.fixture
def coll():
    result = [
        {
            "key": "common",
            "status": "nested",
            "value": [
                {"key": "follow", "status": "added", "value": False},
                {"key": "setting1", "status": "same", "value": "Value 1"},
                {"key": "setting2", "status": "removed", "value": 200},
                {
                    "key": "setting3",
                    "status": "changed",
                    "old_value": True,
                    "new_value": None,
                },
                {"key": "setting4", "status": "added", "value": "blah blah"},
                {"key": "setting5", "status": "added", "value": {"key5": "value5"}},
                {
                    "key": "setting6",
                    "status": "nested",
                    "value": [
                        {
                            "key": "doge",
                            "status": "nested",
                            "value": [
                                {
                                    "key": "wow",
                                    "status": "changed",
                                    "old_value": "",
                                    "new_value": "so much",
                                }
                            ],
                        },
                        {"key": "key", "status": "same", "value": "value"},
                        {"key": "ops", "status": "added", "value": "vops"},
                    ],
                },
            ],
        },
        {
            "key": "group1",
            "status": "nested",
            "value": [
                {
                    "key": "baz",
                    "status": "changed",
                    "old_value": "bas",
                    "new_value": "bars",
                },
                {"key": "foo", "status": "same", "value": "bar"},
                {
                    "key": "nest",
                    "status": "changed",
                    "old_value": {"key": "value"},
                    "new_value": "str",
                },
            ],
        },
        {
            "key": "group2",
            "status": "removed",
            "value": {"abc": 12345, "deep": {"id": 45}},
        },
        {
            "key": "group3",
            "status": "added",
            "value": {"deep": {"id": {"number": 45}}, "fee": 100500},
        },
    ]
    return result


def test_is_key():
    dic = {
        "key": "value",
    }

    assert is_key("key", dic) == True  # noqa
    assert is_key("value", dic) == False  # noqa


def test_get_format_file():
    assert get_format_file("gendiff/tests/fixture/file1.json") == ".json"


def test_get_path_to_file():
    get_path_to_file(
        "gendiff/tests/fixture/file1.json"
    ) == "/home/nikskor/projects/python-project-50/gendiff/tests/fixture/file1.json"


def test_get_data_from_file():
    with open("gendiff/tests/fixture/file1.json", encoding="utf-8") as file1json, open(
        "gendiff/tests/fixture/file1.yaml", encoding="utf-8"
    ) as file1yaml:
        dicjson = json.load(file1json)
        dicyaml = yaml.full_load(file1yaml)
    assert get_data_from_file("gendiff/tests/fixture/file1.json") == dicjson
    assert get_data_from_file("gendiff/tests/fixture/file1.yaml") == dicyaml


def test_get_generate_diff():
    with open(
        "gendiff/tests/fixture/result_generate_diff.txt", "r", encoding="utf-8"
    ) as result, open(
        "gendiff/tests/fixture/nested_result.txt", "r", encoding="utf-8"
    ) as nested_result:
        result = result.read()
        nested_result = nested_result.read()
    assert (
        get_generate_diff(
            "gendiff/tests/fixture/file1.json",
            "gendiff/tests/fixture/file2.json",
        )
        == result
    )
    assert (
        get_generate_diff(
            "gendiff/tests/fixture/file1.yaml",
            "gendiff/tests/fixture/file2.yaml",
        )
        == result
    )
    assert (
        get_generate_diff(
            "gendiff/tests/fixture/file3.json",
            "gendiff/tests/fixture/file4.json",
        )
        == nested_result
    )
    assert (
        get_generate_diff(
            "gendiff/tests/fixture/file3.yaml",
            "gendiff/tests/fixture/file4.yaml",
        )
        == nested_result
    )


def test_get_value():
    bool_value = True
    none_value = None
    list_value = [
        {"status": "added", "value": "something", "key": "fifty"},
        {"status": "added", "value": "something", "key": "fifty"},
    ]
    dict_value = {"status": "added", "value": "something", "key": "fifty"}

    assert get_value(bool_value, 1) == "true"
    assert get_value(none_value, 1) == "null"
    assert (
        get_value(list_value, 1)
        == "{\n  + fifty: something\n  + fifty: something\n}"
    )
    assert (
        get_value(dict_value, 1)
        == "{\n    status: added\n    value: something\n    key: fifty\n}"
    )


def test_get_diff_files(coll):
    with open("gendiff/tests/fixture/file3.json") as file1, open(
        "gendiff/tests/fixture/file4.json"
    ) as file2:
        file1 = json.load(file1)
        file2 = json.load(file2)
    assert get_diff_files(file1, file2) == coll


def test_stylish(coll):
    with open(
        "gendiff/tests/fixture/nested_result.txt", "r", encoding="utf-8"
    ) as file1:
        result = file1.read()
    assert stylish(coll) == result


def test_plain(coll):
    with open(
        "gendiff/tests/fixture/plain_result.txt", "r", encoding="utf-8"
    ) as file1:
        result = file1.read()
        assert plain(coll) == result
