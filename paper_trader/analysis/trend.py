from datetime import datetime, timedelta

from pandas import DataFrame
from scipy import stats

from paper_trader.exchange.history import SymbolPriceTime
from paper_trader.utils.dataclasses import to_pandas
from paper_trader.utils.pandas import rows_count


def trend(data: list[SymbolPriceTime], days: int) -> DataFrame | None:
    df = to_pandas(data)
    if df is None:
        return None

    df = df.loc[df.index > (datetime.utcnow() - timedelta(days=days))]

    result = DataFrame(
        {"symbol": [], "slope": [], "intercept": [], "r": []}
    ).set_index("symbol")

    for symbol in df["symbol"].unique():
        symbol_prices = df[df["symbol"] == symbol].copy()
        initial_price = symbol_prices["price"].to_list()[0]
        normalised_prices = symbol_prices["price"] * (100.0 / initial_price)

        res = stats.linregress(
            list(range(rows_count(symbol_prices))), normalised_prices
        )

        result.loc[symbol] = [symbol, res.slope, res.intercept, res.rvalue]

    result.sort_values("slope", ascending=False, inplace=True)

    return result
