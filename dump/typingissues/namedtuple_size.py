# Pyright issue 1152: https://github.com/microsoft/pyright/issues/1152

from typing import NamedTuple, Tuple


class Tuple1(NamedTuple):
    a: float
    b: float


t: Tuple[float, float] = Tuple1(a=1, b=2)
# Expression of type "Tuple1" cannot be assigned to declared type "Tuple[float, float]"
#  Tuple size mismatch; expected 2 but received 2 Pylance (reportGeneralTypeIssues)
