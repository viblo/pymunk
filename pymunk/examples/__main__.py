import argparse
import os.path
import pathlib
import sys

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


def list_examples() -> None:
    for f in pathlib.Path(__file__).parent.glob("*.py"):
        if f.stem.startswith("__") or not f.is_file():
            continue
        print(f"python -m pymunk.examples.{f.stem}")


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

    args = parser.parse_args(args=None if sys.argv[1:] else ["--help"])
    if args.list:
        list_examples()
    else:
        parser.print_usage()
