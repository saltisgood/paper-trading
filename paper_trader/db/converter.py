from typing import Callable, Dict, Type

_TYPE_CONVERSIONS: Dict[Type, Callable] = {}


def _convert_val_to_db(val):
    try:
        converter = _TYPE_CONVERSIONS[type(val)]
    except KeyError:
        # No registered converter, just return as is
        return val
    else:
        return converter(val)


def _convert_val_from_db(clazz, val):
    try:
        converter = _TYPE_CONVERSIONS[clazz]
    except KeyError:
        return val
    else:
        return converter(db=val)


def register_converter(clazz):
    def f(func):
        _TYPE_CONVERSIONS[clazz] = func
        return func

    return f
