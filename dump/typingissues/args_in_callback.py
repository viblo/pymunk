from typing import Any, Callable, Dict, Tuple

# Not currently possible to specify Callable[[int, args, kwargs], None] as type
# Instead Callable[..., None] has to be used..
# Might be resolved in PEP 612 (for Python 3.10). As of 2020-11-10 only in Pyre, not Pyright or Mypy


def run_callback(
    callback: Callable[..., None], *args: Tuple[Any, ...], **kwargs: Dict[str, Any]
) -> None:
    callback(5, *args, **kwargs)


def f(x: int, y: float) -> None:
    pass


y = 5
run_callback(f, y)
