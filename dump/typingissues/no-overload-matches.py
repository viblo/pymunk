import collections.abc
from typing import Any, Optional, Sequence, Tuple, Union, overload


class Vec(Sequence[float]):
    @overload
    def __init__(self, x_or_pair: Sequence[float], y: None) -> None:
        ...

    @overload
    def __init__(self, x_or_pair: float, y: float) -> None:
        ...

    def __init__(
        self, x_or_pair: Union[Sequence[float], float] = None, y: Optional[float] = None
    ) -> None:
        pass

    @overload
    def __getitem__(self, index: int) -> float:
        ...

    @overload
    def __getitem__(self, index: slice) -> Sequence[float]:
        ...

    def __getitem__(self, index: Union[int, slice]) -> Union[float, Sequence[float]]:
        return 0

    def __len__(self) -> int:
        return 2


Vec((1.0, 2.0))  #
