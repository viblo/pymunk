import timeit
from timeit import repeat

import pymunk

print("pymunk.version", pymunk.version)

s = None


def setup(num_bodies=10):
    global s
    s = pymunk.Space()

    for x in range(num_bodies):
        b = pymunk.Body()
        b.position = x / 5, x / 2
        s.add(b)
    s.step(1)


def non_batched():
    positions = []
    global s
    for b in s.bodies:
        positions.append(b.position.x)
        positions.append(b.position.y)


def batched():
    arr = pymunk.ffi.new("cpVectArr *", {"num": 0})
    arr.num = 0
    arr.max = 0
    pymunk.cp.cpSpaceGetBodyPositions(s._space, arr)
    buf = pymunk.ffi.buffer(arr.arr, pymunk.ffi.sizeof("cpVect") * arr.num)
    mv = memoryview(buf)
    positions = list(mv.cast("d"))


if __name__ == "__main__":
    import timeit

    for num_bodies in [1, 5, 10, 100, 1000, 10000]:
        print(f"Testing bodies:{num_bodies} non-batched", flush=True)
        setup(num_bodies)
        print(
            sorted(
                timeit.repeat(
                    "non_batched()",
                    setup="from __main__ import non_batched",
                    number=int(500_000 // num_bodies),
                )
            )
        )
    for num_bodies in [1, 5, 10, 100, 1000, 10000]:
        print(f"Testing bodies:{num_bodies} batched", flush=True)
        setup(num_bodies)
        print(
            sorted(
                timeit.repeat(
                    "batched()",
                    setup="from __main__ import batched",
                    number=int(500_000 // num_bodies),
                )
            )
        )
