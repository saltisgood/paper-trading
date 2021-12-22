from paper_trader.utils.case import camel_to_snake


def test_camel_to_snake():
    assert camel_to_snake(None) == ""
    assert camel_to_snake("") == ""
    assert camel_to_snake("CamelCase") == "camel_case"
