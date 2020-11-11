from typing import Any, Callable


def func1(callback: Callable[[Any, Any], None], *args: Any, **kwargs: Any):
    callback(*args, **kwargs)  # mypy complains with too many arguments error


def func2(callback: Callable[..., None], *args: Any, **kwargs: Any):
    callback(*args, **kwargs)


def cb(*args: Any, **kwargs: Any) -> None:
    print(args)
    print(kwargs)


func1(cb, 1, 2, three=3, four=4)
func2(cb, 1, 2, three=3, four=4)
