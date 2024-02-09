import json

from gendiff.scripts.gendiff import is_key, generate_diff, get_data_from_file


def test_is_key():
    dic = {
        "key": "value",
    }

    assert is_key("key", dic) == True
    assert is_key("value", dic) == False


def test_get_data_from_file():
    with open("gendiff/tests/fixture/file1.json", encoding="utf-8") as file1:
        dic = json.load(file1)
    assert get_data_from_file("gendiff/tests/fixture/file1.json") == dic


def test_generate_diff():
    with open(
        "gendiff/tests/fixture/result_generate_diff.txt", "r", encoding="utf-8"
    ) as result:
        result = result.read()
    assert (
        generate_diff(
            "gendiff/tests/fixture/file1.json",
            "gendiff/tests/fixture/file2.json",
        )
        == result
    )
