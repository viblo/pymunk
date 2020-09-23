from typing import Callable, List, Tuple

map(lambda x: tuple(x), [[1, 2]])
f: Callable[[List[int]], Tuple[int]] = tuple
map(f, [[1, 2]])  # mypy error here

[tuple(x) for x in [[1, 2]]]
