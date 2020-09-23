from typing import Callable, List, Optional, Tuple


def outer(x: Optional[int]) -> None:
    if x is not None:
        assert x is not None

        def f() -> None:
            x + 1


# already reported as https://github.com/python/mypy/issues/2608
