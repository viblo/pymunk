import os
import sys

# uv run sphinx-build  -E -b html docs/src docs/html

def main():
    os.system("""python -m sphinx  -E -b html ../docs/src ../docs/html""")


if __name__ == "__main__":
    sys.exit(main())
