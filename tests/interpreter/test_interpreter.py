from io import StringIO, SEEK_SET
import pytest
import re

from paper_trader.interpreter.interpreter import BaseInterpreter, add_arg


class TestInterpreter(BaseInterpreter):
    __test__ = False
    prompt = "(tester) "

    def __init__(self, *nargs, **kwargs):
        super().__init__(*nargs, **kwargs)
        self.called = []
        self.use_rawinput = False

    @add_arg("mandatory", type=str, help="This is mandatory")
    @add_arg("-o", "--optional", type=int, default=24, help="This is optional")
    def cmd_test(self, mandatory: str, optional: int):
        self.called.append((mandatory, optional))


@pytest.fixture
def input():
    class Inputter:
        def __init__(self):
            self.stream = StringIO()

        def __call__(self, text: str):
            self.stream.write(text)
            self.stream.seek(SEEK_SET, 0)

    return Inputter()


@pytest.fixture
def output():
    class Outputter:
        def __init__(self):
            self.stream = StringIO()

        def __call__(self):
            return self.stream.getvalue()

    return Outputter()


@pytest.fixture
def interpreter(input, output):
    return TestInterpreter(stdin=input.stream, stdout=output.stream)


PROLOG = "Available commands: exit, help, quit, test\n"


def test_eof(interpreter: TestInterpreter, output):
    interpreter.cmdloop()
    assert output() == f"{PROLOG}(tester) "


def test_help(interpreter: TestInterpreter, input, output):
    input("help\n")
    interpreter.cmdloop()
    assert (
        output()
        == f"{PROLOG}(tester) Available commands: exit, help, quit, test\n(tester) "
    )


def test_cmd_help(interpreter: TestInterpreter, input, output):
    input("help test\n")
    interpreter.cmdloop()
    assert re.match(
        PROLOG
        + r"\(tester\) usage: test \[-o OPTIONAL\] mandatory\n\npositional arguments:\n\s*mandatory\s+This is mandatory\n\noptions:\n\s*-o OPTIONAL, --optional OPTIONAL\n\s*This is optional\n\(tester\)",
        output(),
    )


def test_cmd(interpreter: TestInterpreter, input):
    input("test -o 1 2")
    interpreter.cmdloop()
    assert interpreter.called == [("2", 1)]


def test_bad_args(interpreter: TestInterpreter, input, output):
    input("test\ntest 1 2\ntest -o 3\ntest -o X 4\ntest 5")
    interpreter.cmdloop()
    assert re.search(
        r"\(tester\) the following arguments are required: mandatory\nusage:",
        output(),
    )
    assert re.search(r"\(tester\) unrecognized arguments: 2\nusage:", output())
    # The 3rd fail has the same error as the 1st
    assert re.search(
        r"\(tester\) argument -o/--optional: invalid int value: 'X'\nusage:",
        output(),
    )
    assert interpreter.called == [("5", 24)]


def test_quoted(interpreter: TestInterpreter, input):
    input('test "i am quoted"\n')
    interpreter.cmdloop()
    assert interpreter.called == [("i am quoted", 24)]


def test_quit(interpreter: TestInterpreter, input):
    input("quit\ntest 1")
    interpreter.cmdloop()
    assert not interpreter.called


def test_exit(interpreter: TestInterpreter, input):
    input("exit\ntest 1")
    interpreter.cmdloop()
    assert not interpreter.called


def test_split_line():
    assert BaseInterpreter.split_line("") == ("", [])
    assert BaseInterpreter.split_line("help") == ("help", [])
    assert BaseInterpreter.split_line("help on something else") == (
        "help",
        ["on", "something", "else"],
    )
    assert BaseInterpreter.split_line('help "on something" else') == (
        "help",
        ["on something", "else"],
    )
    assert BaseInterpreter.split_line('help on "something else"') == (
        "help",
        ["on", "something else"],
    )
    assert BaseInterpreter.split_line('help -on ""') == ("help", ["-on", ""])
    assert BaseInterpreter.split_line('help -on "" -and "x"') == (
        "help",
        ["-on", "", "-and", "x"],
    )
