from dataclasses import fields, is_dataclass

from ..case import camel_to_snake
from .decorator import _get_primary_keys, _has_primary_keys


class DataclassDesc:
    def __init__(self, inst=None, clazz=None):
        assert inst is not None or clazz is not None
        if inst is not None:
            typ = type(inst)
        else:
            typ = clazz
        v = inst if inst is not None else clazz
        assert is_dataclass(v)
        self._name = camel_to_snake(typ.__name__)
        self._fields = {f.name: f.type for f in fields(v)}
        self._field_types = [f.type for f in fields(v)]
        if _has_primary_keys(v):
            self._primary_keys = _get_primary_keys(v)
        else:
            self._primary_keys = []

    @property
    def name(self):
        return self._name

    @property
    def fields(self):
        return self._fields

    @property
    def field_types(self):
        return self._field_types

    @property
    def has_primary_keys(self):
        return bool(self._primary_keys)

    @property
    def primary_keys_names(self):
        return self._primary_keys

    def get_primary_keys(self, inst):
        return [getattr(inst, pk) for pk in self.primary_keys_names]

    def get_fields(self, inst):
        return [getattr(inst, f) for f in self.fields]
