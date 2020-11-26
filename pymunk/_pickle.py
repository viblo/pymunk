import copy
from typing import Any, ClassVar, Dict, List, Tuple, TypeVar

T = TypeVar("T", bound="PickleMixin")
_State = Dict[str, List[Tuple[str, Any]]]


class PickleMixin:
    """PickleMixin is used to provide base functionality for pickle/unpickle
    and copy.
    """

    _pickle_attrs_init: ClassVar[List[str]] = []
    _pickle_attrs_general: ClassVar[List[str]] = []
    _pickle_attrs_skip: ClassVar[List[str]] = []

    def __getstate__(self) -> _State:
        """Return the state of this object

        This method allows the usage of the :mod:`copy` and :mod:`pickle`
        modules with this class.
        """

        d: _State = {
            "init": [],  # arguments for init
            "general": [],  # general attributes
            "custom": [],  # custom attributes set by user
            "special": [],  # attributes needing special handling
        }
        for a in type(self)._pickle_attrs_init:
            d["init"].append((a, self.__getattribute__(a)))

        for a in type(self)._pickle_attrs_general:
            d["general"].append((a, self.__getattribute__(a)))

        for k, v in self.__dict__.items():
            if k[0] != "_":
                d["custom"].append((k, v))

        return d

    def __setstate__(self, state: _State) -> None:
        """Unpack this object from a saved state.

        This method allows the usage of the :mod:`copy` and :mod:`pickle`
        modules with this class.
        """

        init_attrs: List[str] = []

        init_args = [v for k, v in state["init"]]
        self.__init__(*init_args)  # type: ignore

        for k, v in state["general"]:
            self.__setattr__(k, v)

        for k, v in state["custom"]:
            self.__setattr__(k, v)

    def copy(self: T) -> T:
        """Create a deep copy of this object."""
        return copy.deepcopy(self)
