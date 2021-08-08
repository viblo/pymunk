from typing import Tuple, Union, overload


@overload
def f1(t: Tuple[int]) -> Tuple[int]:
    ...


@overload
def f1(t: Tuple[int, int]) -> Tuple[int, int]:
    ...


def f1(t: Union[Tuple[int], Tuple[int, int]]) -> Union[Tuple[int], Tuple[int, int]]:
    if len(t) == 1:
        a = t
        return (a,)
    else:
        a, b = t
        return a, b


# As of 2021-08-08, errors in both Pylance & Mypy
# Mypy errors:
# overload_tuple_lengths.py:17: error: Incompatible return value type (got "Tuple[Union[Tuple[int], Tuple[int, int]]]", expected "Union[Tuple[int], Tuple[int, int]]")
# overload_tuple_lengths.py:19: error: Need more than 1 value to unpack (2 expected)
# overload_tuple_lengths.py:19: error: Incompatible types in assignment (expression has type "int", variable has type "Union[Tuple[int], Tuple[int, int]]")
# overload_tuple_lengths.py:20: error: Incompatible return value type (got "Tuple[Union[Tuple[int], Tuple[int, int]], Union[Any, int]]", expected "Union[Tuple[int], Tuple[int, int]]")

# Can be handled with PEP 647 https://www.python.org/dev/peps/pep-0647/ in Pyhton 3.10
# Workarounds:
# a,b = cast(Tuple[float, float], t)
# or
# a,b = t # type: ignore
