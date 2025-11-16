import array
import timeit

import pymunk
import pymunk.batch

print("pymunk.version", pymunk.version)

space: pymunk.Space = pymunk.Space()
get_buffer: pymunk.batch.Buffer = pymunk.batch.Buffer()
set_buffer: pymunk.batch.Buffer = pymunk.batch.Buffer()
set_array: array.array


def setup(num_bodies: int = 10) -> None:
    global space
    global get_buffer
    global set_buffer
    global set_array

    space = pymunk.Space()
    get_buffer = pymunk.batch.Buffer()
    set_buffer = pymunk.batch.Buffer()
    set_array = array.array("d", [1, 2, 3] * num_bodies)

    for x in range(num_bodies):
        b = pymunk.Body()
        b.position = x / 5, x / 2
        b.angle = x / 3
        space.add(b)
    space.step(1)


def normal_get() -> None:
    res = 0

    for b in space.bodies:
        res += b.position.x + b.position.y + b.angle
    _ = res


def normal_set() -> None:
    for b in space.bodies:
        b.position = 1, 2
        b.angle = 4


def batch_get() -> None:
    get_buffer.clear()
    pymunk.batch.get_space_bodies(
        space,
        pymunk.batch.BodyFields.POSITION | pymunk.batch.BodyFields.ANGLE,
        get_buffer,
    )
    _ = sum(memoryview(get_buffer.float_buf()).cast("d"))


def batch_set() -> None:
    set_buffer.set_float_buf(set_array)
    pymunk.batch.set_space_bodies(
        space,
        pymunk.batch.BodyFields.POSITION | pymunk.batch.BodyFields.ANGLE,
        set_buffer,
    )


def print_results(test, res):
    print(test)
    for k, v in res.items():
        line = f"{k:<8}" + f"{v[0]:<8,.2f}" + f"{v[1]:<8,.2f}"
        print(line)


if __name__ == "__main__":
    import timeit

    funcs = [
        "normal_get",
        "batch_get",
        "normal_set",
        "batch_set",
    ]

    for func in funcs:
        print(f"{func}")
        print("========")
        for num_bodies in [1, 5, 10, 100, 1000, 10000, 50000, 100000]:
            if func.startswith("normal") and num_bodies > 100:
                x = 0
            else:
                setup(num_bodies)
                x = min(
                    timeit.repeat(
                        f"{func}()",
                        setup=f"from __main__ import {func}",
                        number=1_000_000 // num_bodies,
                    )
                )
            line = f"{num_bodies:<8}" + f"{x:<8,.2f}"
            print(line)
