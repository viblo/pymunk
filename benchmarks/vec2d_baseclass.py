"""Test different ways to implement Vec2d.

Compares:
    - Object and NamedTuple as base classes
    - Ways to create a Vec2d.
"""

from typing import NamedTuple

import pymunk

print("pymunk.version", pymunk.version)

s = None
g = None
vec_obj = None
vec_ntuple = None


def setup():
    global s
    global g
    global vec_obj
    global vec_ntuple
    s = pymunk.Space()
    s.gravity = 123, 456
    g = pymunk.cp.cpSpaceGetGravity(s._space)
    vec_obj = Vec2dObject(123, 456)
    vec_ntuple = Vec2dNamedTuple(123, 456)


# 1 Vec2d with object as baseclass
class Vec2dObject:
    __slots__ = ("x", "y")

    x: float
    y: float

    @staticmethod
    def _fromcffi(p) -> "Vec2dObject":
        """Used as a speedy way to create Vec2ds internally in pymunk."""
        v = Vec2dObject.__new__(Vec2dObject)
        v.x = p.x
        v.y = p.y
        return v

    def __init__(self, x_or_pair, y=None):
        if y is None:
            if isinstance(x_or_pair, Vec2dObject):
                self.x = x_or_pair.x
                self.y = x_or_pair.y
            else:
                assert (
                    len(x_or_pair) == 2
                ), f"{x_or_pair} must be of length 2 when used alone"
                self.x = x_or_pair[0]
                self.y = x_or_pair[1]
        else:
            self.x = x_or_pair
            self.y = y

    def __getitem__(self, i):
        if i == 0:
            return self.x
        elif i == 1:
            return self.y
        raise IndexError()

    def __iter__(self):
        yield self.x
        yield self.y

    def __len__(self) -> int:
        return 2

    # String representaion (for debugging)
    def __repr__(self) -> str:
        return f"Vec2dObject({self.x}, {self.y})"

    # Comparison
    def __eq__(self, other) -> bool:
        if hasattr(other, "__getitem__") and len(other) == 2:
            return self.x == other[0] and self.y == other[1]
        else:
            return False

    def __ne__(self, other) -> bool:
        if hasattr(other, "__getitem__") and len(other) == 2:
            return self.x != other[0] or self.y != other[1]
        else:
            return True


class Vec2dNamedTuple(NamedTuple):

    x: float
    y: float

    @staticmethod
    def _fromcffi(p) -> "Vec2dNamedTuple":
        """Used as a speedy way to create Vec2ds internally in pymunk."""
        return Vec2dNamedTuple.__new__(Vec2dNamedTuple, p.x, p.y)

    @staticmethod
    def _fromcffi2(p) -> "Vec2dNamedTuple":
        """Used as a speedy way to create Vec2ds internally in pymunk."""
        return Vec2dNamedTuple(p.x, p.y)


# Benchmarks
def bench_creation_constructor():
    g2 = g
    gr = Vec2dNamedTuple(g2.x, g2.y)


# not supported:
# def bench_creation_constructor_unpack():
#     gr = Vec2dNamedTuple(*g)


def bench_creation_fromcffi():
    gr = Vec2dNamedTuple._fromcffi(g)


def bench_creation_fromcffi2():
    gr = Vec2dNamedTuple._fromcffi2(g)


def bench_creation_usingnew():
    gr = Vec2dNamedTuple.__new__(Vec2dNamedTuple, g.x, g.y)


def bench_set_vec_obj():
    pymunk.cp.cpSpaceSetGravity(s._space, tuple(vec_obj))


def bench_set_vec_ntuple_wrapped():
    pymunk.cp.cpSpaceSetGravity(s._space, tuple(vec_ntuple))


def bench_set_vec_ntuple():
    assert len(vec_ntuple) == 2
    pymunk.cp.cpSpaceSetGravity(s._space, vec_ntuple)


def run_bench(func):
    print(f"Running {func}")
    print(
        sorted(
            timeit.repeat(
                f"{func}()",
                setup=f"from __main__ import {func}",
            )
        )
    )


if __name__ == "__main__":
    import timeit

    print("Benchmark: Compare ways to construct Vec2ds")
    setup()
    run_bench("bench_creation_constructor")
    run_bench("bench_creation_fromcffi")
    run_bench("bench_creation_fromcffi2")
    run_bench("bench_creation_usingnew")
    run_bench("bench_set_vec_obj")
    run_bench("bench_set_vec_ntuple_wrapped")
    run_bench("bench_set_vec_ntuple")
