from decimal import Decimal

from paper_trader.utils.price import DecimalConverter, Price, PriceConverter


def test_init_price():
    p = Price("123.45")
    assert p == Price(Decimal("123.45"))
    assert p.value == Decimal("123.45")

    p2 = Price("54.321")
    assert p != p2

    p.value = "54.321"
    assert p == p2


def test_price_converter():
    p = Price("328.29")
    conv = PriceConverter
    p_db = conv.to_db(p)
    assert type(p_db) is str
    assert p_db == "328.2900"

    p2 = conv.from_db(p_db)
    assert type(p2) is Price
    assert p == p2


def test_decimal_to_db():
    d = Decimal("6543.11")
    conv = DecimalConverter
    d_db = conv.to_db(d)
    assert type(d_db) is str
    assert d_db == "6543.11"

    d2 = conv.from_db(d_db)
    assert type(d2) is Decimal
    assert d == d2
