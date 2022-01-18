import sqlite3
from dataclasses import fields, is_dataclass
from typing import Any, Iterable

from ..utils.case import camel_to_snake
from .converter import _convert_val_from_db, _convert_val_to_db
from .decorator import _get_primary_keys


class _ClassDesc:
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
        self._primary_keys = _get_primary_keys(v)

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
    def primary_keys_names(self):
        return self._primary_keys

    @property
    def create_table_str(self):
        cols = ", ".join(self.fields.keys())
        pks = "PRIMARY KEY ({})".format(
            ", ".join(k for k in self.primary_keys_names)
        )
        return f"CREATE TABLE IF NOT EXISTS {self.name} ({cols}, {pks})"

    @property
    def upsert_str(self):
        return f'INSERT OR REPLACE INTO {self.name} VALUES ({", ".join("?" for _ in range(len(self.fields)))})'

    @property
    def delete_str(self):
        return f"DELETE FROM {self.name} WHERE " + " AND ".join(
            f"{pk}=?" for pk in self.primary_keys_names
        )

    @property
    def get_all_str(self):
        return f"SELECT * FROM {self.name}"

    def get_primary_keys(self, inst):
        return [getattr(inst, pk) for pk in self.primary_keys_names]

    def get_fields(self, inst):
        return [_convert_val_to_db(getattr(inst, f)) for f in self.fields]


class SqliteDb:
    def __init__(self, filename: str):
        self._db = sqlite3.connect(filename)

    def __enter__(self):
        self._db.__enter__()
        return self

    # NOTE: This just commits or rolls back doesn't close the connection, bit misleading
    def __exit__(self, exc_type, exc_value, traceback):
        self._db.__exit__(exc_type, exc_value, traceback)

    def close(self):
        self._db.close()
        self._db = None

    def init_table(self, clazz):
        desc = _ClassDesc(clazz=clazz)
        cursor = self._db.cursor()
        cursor.execute(desc.create_table_str)

    def upsert(self, obj: Any):
        desc = _ClassDesc(inst=obj)
        cursor = self._db.cursor()
        cursor.execute(desc.upsert_str, desc.get_fields(obj))

    def upsert_all(self, objs: Iterable):
        desc = None
        cursor = self._db.cursor()
        for obj in objs:
            if desc is None:
                desc = _ClassDesc(inst=obj)
            cursor.execute(desc.upsert_str, desc.get_fields(obj))

    def delete(self, obj):
        desc = _ClassDesc(inst=obj)
        cursor = self._db.cursor()
        cursor.execute(desc.delete_str, desc.get_primary_keys(obj))

    def get_all(self, clazz):
        desc = _ClassDesc(clazz=clazz)
        for vals in self._db.cursor().execute(desc.get_all_str).fetchall():
            yield clazz(
                *(
                    _convert_val_from_db(t, v)
                    for t, v in zip(desc.field_types, vals)
                )
            )

    def commit(self):
        self._db.commit()

    def rollback(self):
        self._db.rollback()
