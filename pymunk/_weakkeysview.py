from collections.abc import Iterator, KeysView
from typing import TYPE_CHECKING, TypeVar
from weakref import WeakKeyDictionary

# Can be simplified in Python 3.12, PEP 695
KT = TypeVar("KT")
VT = TypeVar("VT")


class WeakKeysView(KeysView[KT]):
    def __init__(self, weak_dict: WeakKeyDictionary[KT, VT]) -> None:
        self._weak_dict = weak_dict

    def __iter__(self) -> Iterator[KT]:
        return iter(self._weak_dict.keys())

    def __len__(self) -> int:
        return len(self._weak_dict)

    def __contains__(self, key: object) -> bool:
        return key in self._weak_dict

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({list(self._weak_dict.keys())})"
