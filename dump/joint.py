import pymunk

a, b = pymunk.Body(1, 2), pymunk.Body(1, 2)
c = pymunk.CustomConstraint(a, b)

space = pymunk.Space()

space.add(a, b, c)

space.step(1)
space.step(0.1)
