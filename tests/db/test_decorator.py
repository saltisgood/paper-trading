from paper_trader.db.decorator import primary_key, _get_primary_keys

@primary_key('a', 'b')
class Foo:
    a = 1
    b = 2
    c = 3

def test_primary_keys():
    keys = _get_primary_keys(Foo)
    assert keys == ['a', 'b']
