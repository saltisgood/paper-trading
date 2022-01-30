import argparse  # pragma: no cover

from paper_trader.interpreter.interpreter import BaseInterpreter


def main() -> None:  # pragma: no cover
    """
    The main function executes on commands:
    `python -m paper_trader` and `$ paper_trader `.

    This is your program's entry point.

    You can change this function to do whatever you want.
    Examples:
        * Run a test suite
        * Run a server
        * Do some other stuff
        * Run a command line application (Click, Typer, ArgParse)
        * List all available tasks
        * Run an application (Flask, FastAPI, Django, etc.)
    """
    parser = argparse.ArgumentParser(
        description="paper_trader.",
        epilog="Enjoy the paper_trader functionality!",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Optionally adds verbosity",
    )
    args = parser.parse_args()
    if args.verbose:
        print("Verbose mode is on.")

    BaseInterpreter().cmdloop()


if __name__ == "__main__":  # pragma: no cover
    main()
