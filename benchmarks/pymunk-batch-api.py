import timeit

import pymunk
import pymunk.batch

print("pymunk.version", pymunk.version)

space: pymunk.Space = pymunk.Space()


def setup(num_bodies: int = 10) -> None:
    global space
    space = pymunk.Space()

    for x in range(num_bodies):
        b = pymunk.Body()
        b.position = x / 5, x / 2
        b.angle = x / 3
        space.add(b)
    space.step(1)


def non_batched() -> None:
    res = 0

    for b in space.bodies:
        res += b.position.x + b.position.y + b.angle
    _ = res


buffers = pymunk.batch.Buffer()


def batched():
    buffers.clear()
    pymunk.batch.get_space_bodies(
        space, pymunk.batch.BodyFields.POSITION | pymunk.batch.BodyFields.ANGLE, buffers
    )
    _ = sum(memoryview(buffers.float_buf()).cast("d"))


if __name__ == "__main__":
    import timeit

    for num_bodies in [1, 5, 10, 100, 1000]:
        print(f"Testing bodies:{num_bodies} non-batched", flush=True)
        setup(num_bodies)
        print(
            sorted(
                timeit.repeat(
                    "non_batched()",
                    setup="from __main__ import non_batched",
                    number=1_000_000 // num_bodies,
                )
            )
        )
    for num_bodies in [1, 5, 10, 100, 1000, 10000, 50000, 100000]:
        print(f"Testing bodies:{num_bodies} batched", flush=True)
        setup(num_bodies)
        print(
            sorted(
                timeit.repeat(
                    "batched()",
                    setup="from __main__ import batched",
                    number=1_000_000 // num_bodies,
                )
            )
        )
