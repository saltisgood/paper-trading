from paper_trader.db.converter import (
    register_converter,
    _convert_val_from_db,
    _convert_val_to_db,
)


class Foo:
    def __init__(self, x):
        self._x = x


@register_converter(Foo)
def conv(f: Foo = None, db: str = None):
    if f is not None:
        return str(f._x)
    assert db is not None
    return Foo(int(db))


def test_convertor():
    f = Foo(123)
    f_str = _convert_val_to_db(f)
    assert type(f_str) is str
    assert f_str == "123"

    f2 = _convert_val_from_db(Foo, f_str)
    assert type(f2) is Foo
    assert f2._x == 123


def test_default_convertor():
    s = 7456
    x = _convert_val_to_db(s)
    assert type(x) is int
    assert x == s

    s2 = _convert_val_from_db(int, x)
    assert type(s2) is int
    assert s == s2
