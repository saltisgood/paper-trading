from dataclasses import dataclass

from paper_trader.db.decorator import primary_key
from paper_trader.db.sqlite import SqliteDb


@dataclass
@primary_key("a", "b")
class Foo:
    a: str
    b: int
    c: str


def test_sqlite_upsert():
    db = SqliteDb("t1.db3")

    with db:
        db.init_table(Foo)

        db.upsert(Foo("s1", 987, "e1"))

    with db:
        foos = list(db.get_all(Foo))
        assert len(foos) == 1
        assert foos[0] == Foo("s1", 987, "e1")

    with db:
        db.upsert(Foo("s1", 987, "e2"))

    with db:
        foos = list(db.get_all(Foo))
        assert len(foos) == 1
        assert foos[0] == Foo("s1", 987, "e2")

    with db:
        db.upsert(Foo("s2", 987, "e3"))

    with db:
        foos = list(db.get_all(Foo))
        assert len(foos) == 2
        assert Foo("s2", 987, "e3") in foos


def test_sqlite_delete():
    db = SqliteDb("t2.db3")

    with db:
        db.init_table(Foo)

        db.upsert(Foo("s1", 987, "e1"))
        db.upsert(Foo("s2", 123, "e2"))

    with db:
        db.delete(Foo("s1", 987, "e1"))

    with db:
        foos = list(db.get_all(Foo))
        assert len(foos) == 1
        assert foos[0] == Foo("s2", 123, "e2")


def test_sqlite_rollback():
    db = SqliteDb("t3.db3")

    with db:
        db.init_table(Foo)

    with db:
        db.upsert(Foo("s1", 987, "e1"))
        db.rollback()

    with db:
        foos = list(db.get_all(Foo))
        assert not foos

    # Automatic rollback on exceptions
    try:
        with db:
            db.upsert(Foo("s1", 987, "e1"))
            raise Exception()
    except Exception:
        pass

    with db:
        foos = list(db.get_all(Foo))
        assert not foos
