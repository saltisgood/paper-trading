from typing import Iterable

from pandas import DataFrame

from ..price import Price
from .desc import DataclassDesc


def _to_pandas_format(values_map: dict):
    for key in values_map.keys():
        if isinstance(values_map[key][0], Price):
            values_map[key] = [float(x.value) for x in values_map[key]]


def to_pandas(items: Iterable):
    objs = list(items)
    if not objs:
        return None

    desc = DataclassDesc(inst=objs[0])

    values = {}
    for field_name, _ in desc.fields.items():
        values[field_name] = [getattr(obj, field_name) for obj in objs]

    _to_pandas_format(values)

    df = DataFrame(values)
    if desc.has_primary_keys:
        df = df.set_index(desc.primary_keys_names)
    return df
