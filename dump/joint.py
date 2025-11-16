import pymunk
import pymunk.CustomConstraint

a, b = pymunk.Body(1, 2), pymunk.Body(1, 2)
c = pymunk.CustomConstraint.CustomConstraint(a, b)

space = pymunk.Space()

space.add(a, b, c)

space.step(1)
space.step(0.1)
