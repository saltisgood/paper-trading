from typing import Any, Dict, Protocol, Type


class Converter(Protocol):
    @staticmethod
    def from_db(value: Any) -> Any:
        raise NotImplementedError()

    @staticmethod
    def to_db(value: Any) -> Any:
        raise NotImplementedError()


_TYPE_CONVERSIONS: Dict[Type, Converter] = {}


def _convert_val_to_db(val: Any) -> Any:
    try:
        converter = _TYPE_CONVERSIONS[type(val)]
    except KeyError:
        # No registered converter, just return as is
        return val
    else:
        return converter.to_db(val)


def _convert_val_from_db(clazz: Type, val: Any) -> Any:
    try:
        converter = _TYPE_CONVERSIONS[clazz]
    except KeyError:
        return val
    else:
        return converter.from_db(val)


def register_converter(t: Type):
    def f(clazz):
        _TYPE_CONVERSIONS[t] = clazz
        return clazz

    return f
