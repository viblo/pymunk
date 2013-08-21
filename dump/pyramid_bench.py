"""Basic benchmark of a pyramid of boxes

Results with 10000 iterations (lower is better)
python 2.6: 186.8 sec
pypy-1.9: 428.9 sec
"""

import timeit

import pymunk
from pymunk import Vec2d


class PyramidDemo:
    def flipyv(self, v):
        return v[0], -v[1]+self.h
        
    def __init__(self):
        self.running = True
        self.drawing = True
        self.w, self.h = 600,600

        ### Init pymunk and create space
        self.space = pymunk.Space()
        self.space.gravity = (0.0, -900.0)
        ### ground
        body = pymunk.Body()
        shape = pymunk.Segment(body, (50, 100), (550,100), .0)
        shape.friction = 1.0
        self.space.add(shape)
        
        ### pyramid
        x=Vec2d(-100, 7.5) + (300,100)
        y=Vec2d(0,0) 
        deltaX=Vec2d(0.5625, 2.0)*10
        deltaY=Vec2d(1.125, 0.0)*10

        for i in range(25):
            y = Vec2d(x)
            for j in range(i, 25):
                size= 5
                points = [(-size, -size), (-size, size), (size,size), (size, -size)]
                mass = 1.0
                moment = pymunk.moment_for_poly(mass, points, (0,0))
                body = pymunk.Body(mass, moment)
                body.position = y
                shape = pymunk.Poly(body, points, (0,0))
                shape.friction = 1
                self.space.add(body,shape)
                
                y += deltaY

            x += deltaX
        
    def run(self):
        for x in range(10000):
            self.loop() 
            
    def loop(self):  
        
        steps = 3
        dt = 1.0/120.0/steps            
        for x in range(steps):
            self.space.step(dt)
        self.draw()
        
    def draw(self):       
        #simulate drawing
        for shape in self.space.shapes:
            if shape.body.is_static:
                body = shape.body
                pv1 = self.flipyv(body.position + shape.a.cpvrotate(body.rotation_vector))
                pv2 = self.flipyv(body.position + shape.b.cpvrotate(body.rotation_vector))
                          
            else:
                if shape.body.is_sleeping:
                    continue
                ps = shape.get_vertices()
                ps.append(ps[0])
                
def main():
    t = timeit.Timer('demo.run()', "gc.enable(); from __main__ import PyramidDemo;demo = PyramidDemo()") 
    print(t.timeit(number=1))

if __name__ == '__main__':
    doprof = 0
    if not doprof: 
    
        
        main()
    else:
        import cProfile, pstats
        
        prof = cProfile.run("main()", "profile.prof")
        stats = pstats.Stats("profile.prof")
        stats.strip_dirs()
        stats.sort_stats('cumulative', 'time', 'calls')
        stats.print_stats(30)