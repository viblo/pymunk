print("__init__", __name__, __file__)


def init() -> None:
    print("init")


if __name__ == "__main__":
    import os
    import sys

    # sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    init()
