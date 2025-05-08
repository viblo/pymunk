import timeit

s = """
import pymunk
# print("pymunk.version", pymunk.version)
s = pymunk.Space()
s.add(pymunk.Circle(s.static_body, 5))
b = pymunk.Body(1,10)
c = pymunk.Circle(b, 5)
s.add(b, c)
h = s.add_global_collision_handler()
def f(arb, s, data):
    return False
h.pre_solve = f
"""

print(min(timeit.repeat("s.step(0.01)", setup=s, repeat=10)))
