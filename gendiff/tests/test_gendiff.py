import json
import yaml

from gendiff.compare_files import (
    is_key,
    get_diff_between_files,
    get_data_from_file,
    get_format_file,
    get_path_to_file,
)


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


def test_get_diff_between_files():
    with open(
        "gendiff/tests/fixture/result_generate_diff.txt", "r", encoding="utf-8"
    ) as result:
        result = result.read()
    assert (
        get_diff_between_files(
            "gendiff/tests/fixture/file1.json",
            "gendiff/tests/fixture/file2.json",
        )
        == result
    )
    assert (
        get_diff_between_files(
            "gendiff/tests/fixture/file1.yaml",
            "gendiff/tests/fixture/file2.yaml",
        )
        == result
    )
