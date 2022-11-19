import gc
import multiprocessing
import random

import pymunk

random.seed(0)

loops = 20
num_objects = 200


d = {}


def f(x):

    print(f"loop {x}/{loops}")
    s = pymunk.Space()

    for x in range(num_objects):
        b = pymunk.Body(10, 20)

        c = lambda: pymunk.Circle(b, 10)
        e = lambda: pymunk.Segment(b, (-10, 0), (10, 0), 5)
        p = lambda: pymunk.Poly.create_box(b)

        shape = random.choice([c, e, p])()

        if random.random() > 0.9:
            o = random.choice([shape, b])
            d[o] = True
        if random.random() > 0.99 and len(d) > 10:
            k = random.choice(list(d.keys()))
            del d[k]

        b.position = random.randint(0, 100), random.randint(0, 100)
        # if random.random() > 0.99:
        #     gc.collect()
        s.add(b, shape)

    for x in range(num_objects):
        a, b = random.choices(s.bodies, k=2)
        if a == b:
            continue
        c = pymunk.PinJoint(a, b)
        s.add(c)

    for x in range(100):
        s.step(0.02)

    # if random.random() > 0.75:
    #     gc.collect()


def start_pool():
    print("Starting", multiprocessing.current_process().name)


if __name__ == "__main__":
    for x in range(4):
        with multiprocessing.Pool(processes=4, initializer=start_pool) as pool:
            r = pool.map(f, range(loops))

    # print(len(d))
    print("done")
