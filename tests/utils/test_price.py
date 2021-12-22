from decimal import Decimal

from paper_trader.utils.price import Price, decimal_to_db, price_to_db


def test_init_price():
    p = Price("123.45")
    assert p == Price(Decimal("123.45"))
    assert p.value == Decimal("123.45")

    p2 = Price("54.321")
    assert p != p2

    p.value = "54.321"
    assert p == p2


def test_price_to_db():
    p = Price("328.29")
    p_db = price_to_db(p)
    assert type(p_db) is str
    assert p_db == "328.2900"

    p2 = price_to_db(db=p_db)
    assert type(p2) is Price
    assert p == p2


def test_decimal_to_db():
    d = Decimal("6543.11")
    d_db = decimal_to_db(d)
    assert type(d_db) is str
    assert d_db == "6543.11"

    d2 = decimal_to_db(db=d_db)
    assert type(d2) is Decimal
    assert d == d2
