import timeit

s = """
import pymunk
print("pymunk.version", pymunk.version)
s = pymunk.Space()
b = pymunk.Body(1,10)
def f(b,dt):
    b.position += (1,0)
b.position_func = f 
s.add(b)
"""

print(min(timeit.repeat("s.step(0.01)", setup=s, repeat=10)))
