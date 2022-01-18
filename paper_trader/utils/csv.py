from csv import excel, register_dialect, writer
from dataclasses import astuple, fields
from typing import Any, Iterable


class libre(excel):
    lineterminator = "\n"


register_dialect("libre", libre)


class DataclassWriter:
    @staticmethod
    def get_field_names(t: type):
        return [f.name for f in fields(t)]

    def __init__(self, f, t: type, dialect="libre"):
        self._writer = writer(f, dialect=dialect)
        self._writer.writerow(DataclassWriter.get_field_names(t))

    def write_row(self, obj: Any):
        self._writer.writerow(astuple(obj))

    def write_rows(self, objs: Iterable):
        self._writer.writerows(astuple(obj) for obj in objs)
