from argparse import ArgumentError, ArgumentParser
from cmd import Cmd


class _CmdLineParser(ArgumentParser):
    """
    An extension to ArgumentParser set up for interpreter line parsing
    """

    def __init__(self, *nargs, **kwargs):
        super().__init__(add_help=False, exit_on_error=False, *nargs, **kwargs)

    def error(self, msg):
        raise Exception(msg)


def add_arg(*nargs, **kwargs):
    """
    Add an argument to the command. Takes the same arguments as ArgumentParser.add_argument
    """

    def registerer(func):
        if not hasattr(func, "_parser"):
            func._parser = _CmdLineParser(prog=func.__name__[4:])
        func._parser.add_argument(*nargs, **kwargs)
        return func

    return registerer


class BaseInterpreter(Cmd):
    """
    To use:
    Subclass and add commands by adding methods with the name 'cmd_foo'
    Add arguments to the command using the add_arg decorator.
    """

    intro = "Type help of ? to list commands\n"
    prompt = "(paper-trader) "

    def __init__(self, *nargs, **kwargs):
        super().__init__(*nargs, **kwargs)

        self._parsers = dict[str, ArgumentParser]()
        for cmd_func in dir(self):
            if not cmd_func.startswith("cmd_"):
                continue
            func = getattr(self, cmd_func)
            self._parsers[cmd_func[4:]] = func._parser

        cmds = list(self._parsers.keys())
        cmds.extend(("help", "exit", "quit"))
        cmds.sort()
        self.intro = "Available commands: " + ", ".join(cmds)

    def default(self, line: str):
        cmd, args = BaseInterpreter.split_line(line)
        try:
            parser = self._parsers[cmd]
        except KeyError:
            self.unknown_cmd(cmd)
        else:
            try:
                args = parser.parse_args(
                    args=args
                )  # Doesn't consider quotes at this stage
            except ArgumentError as e:
                print(e, file=self.stdout)
                self.do_help(cmd)
            except Exception as e:
                print(e, file=self.stdout)
                self.do_help(cmd)
            else:
                getattr(self, f"cmd_{cmd}")(**vars(args))

    def do_help(self, line: str | None = None):
        if line:
            self._parsers[line].print_help(self.stdout)
        else:
            print(self.intro, file=self.stdout)

    def do_exit(self, _):
        return True

    def do_quit(self, _):
        return True

    def do_EOF(self, _):
        return True

    def unknown_cmd(self, cmd: str):
        print(f"Unknown command: {cmd}", file=self.stdout)
        self.do_help()

    @staticmethod
    def split_line(line: str):
        split = line.split(" ", 1)
        if len(split) > 1:
            cmd = split[0]
            rest = split[1]
        else:
            cmd = split[0]
            rest = None

        params = []
        if rest:
            quote_split = []
            while rest.count('"') > 1:
                first = rest.index('"')
                second = rest.index('"', first + 1)

                before = rest[:first]
                if before:
                    quote_split.append((before, False))
                # fmt: off
                quoted = rest[first + 1: second]
                quote_split.append((quoted, True))
                rest = rest[second + 1:]
                # fmt: on

            if rest:
                quote_split.append((rest, False))

            for s, is_quoted in quote_split:
                if is_quoted:
                    params.append(s)
                else:
                    params.extend(s for s in s.split(" ") if s)

        return cmd, params
