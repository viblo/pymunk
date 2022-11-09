import argparse
import importlib
import os.path
import pathlib
import sys
from typing import Iterable

if sys.argv[0].endswith("__main__.py"):
    # We change sys.argv[0] to make help message more useful
    # use executable without path, unquoted
    # (it's just a hint anyway)
    # (if you have spaces in your executable you get what you deserve!)
    executable = os.path.basename(sys.executable)
    sys.argv[0] = executable + " -m pymunk.examples"

desc = """
Run examples showcasing different aspects of Pymunk. Each example is a module, 
and you run them as you would any module. For example, to run the basic_test 
example, do 

    python -m pymunk.examples.basic_text

"""


def find_examples() -> Iterable[str]:
    for f in pathlib.Path(__file__).parent.glob("*.py"):
        if f.stem.startswith("__") or not f.is_file():
            continue
        yield f.stem


def list_examples() -> None:
    for e in find_examples():
        print(f"python -m pymunk.examples.{e}")


def run_examples() -> None:
    for e in find_examples():
        try:
            m = importlib.import_module("pymunk.examples." + e)
            m.main()
        except Exception as err:
            print(err)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=desc, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "-l",
        "--list",
        help="list all examples as ready to run statements",
        action="store_true",
    )

    # commented out for now since many examples cant handle beeing run in this way.
    # parser.add_argument(
    #     "-a",
    #     "--run-all",
    #     help="run all examples, one by one (useful when testing)",
    #     action="store_true",
    # )

    args = parser.parse_args(args=None if sys.argv[1:] else ["--help"])
    if args.list:
        list_examples()
    # elif args.run_all:
    #     run_examples()
    else:
        parser.print_usage()
