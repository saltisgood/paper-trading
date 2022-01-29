from dataclasses import dataclass

from paper_trader.utils.dataclasses import primary_key, to_pandas
from paper_trader.utils.pandas import rows_count
from paper_trader.utils.price import Price


@dataclass
class DataclassNoPk:
    a: str
    b: int


@primary_key("c")
@dataclass
class DataclassWithPk:
    a: str
    b: Price
    c: str


def test_to_pandas():
    df = to_pandas([])
    assert df is None

    df = to_pandas([DataclassNoPk("str1", 1), DataclassNoPk("str2", 2)])
    assert df is not None
    assert df.size == 4  # 2 rows x 2 cols
    assert rows_count(df.loc[((df["a"] == "str1") & (df["b"] == 1))]) == 1
    assert rows_count(df.loc[((df["a"] == "str2") & (df["b"] == 2))]) == 1

    df = to_pandas(
        [
            DataclassWithPk("abc1", Price("12.34"), "2def"),
            DataclassWithPk("ghi3", Price("43.21"), "jkl4"),
        ]
    )
    assert df is not None
    assert df.size == 4  # 2 rows x 3 cols (-1 index)
    row = df.loc[((df["a"] == "abc1") & (df["b"] == 12.34))]
    assert rows_count(row) == 1
    assert row.index[0] == "2def"
    row = df.loc[((df["a"] == "ghi3") & (df["b"] == 43.21))]
    assert rows_count(row) == 1
    assert row.index[0] == "jkl4"
