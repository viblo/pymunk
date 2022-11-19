"""This example lets you dynamically create static walls and dynamic balls

"""
__docformat__ = "reStructuredText"

import pygame

import pymunk
import pymunk.pygame_util

pm = pymunk


def main():

    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()
    running = True
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    draw_options.flags = pymunk.SpaceDebugDrawOptions.DRAW_SHAPES
    draw_options.flags |= pymunk.SpaceDebugDrawOptions.DRAW_COLLISION_POINTS

    ### Physics stuff
    space = pymunk.Space()

    static_body = space.static_body
    walls = [
        pymunk.Segment(static_body, (0, 0), (0, 150), 0.0),
        pymunk.Segment(static_body, (0, 150), (150, 150), 0.0),
        pymunk.Segment(static_body, (150, 150), (150, 50), 0.0),
        pymunk.Segment(static_body, (150, 50), (100, 50), 0.0),
        pymunk.Segment(static_body, (100, 50), (100, 0), 0.0),
        pymunk.Segment(static_body, (100, 0), (0, 0), 0.0),
    ]
    for wall in walls:
        wall.collision_type = 3
    space.add(*walls)

    x_offset = 5
    y_offset = 5
    sensor_depth = 50
    # body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    body = pymunk.Body(1, 2)
    sensor_shape = pymunk.Poly(
        body,
        [
            (-5 + x_offset, 0 + y_offset),
            (-20 + x_offset, sensor_depth + y_offset),
            (20 + x_offset, sensor_depth + y_offset),
            (5 + x_offset, 0 + y_offset),
        ],
    )
    sensor_shape.sensor = False
    sensor_shape.collision_type = 1

    obj = {}

    def sensor_pre_solve(arbiter: pymunk.Arbiter, space, data):
        if sensor_shape in arbiter.shapes:
            obj["last_set"] = arbiter.contact_point_set
            # for point in arbiter.contact_point_set.points:
            #     obj["last_contact_points"].append((point.point_a, pygame.Color('red'))
            #     obj["last_contact_points"].append((point.point_b, pygame.Color('green'))
        return True

    sensor_collision_handler = space.add_collision_handler(1, 3)
    sensor_collision_handler.pre_solve = sensor_pre_solve
    space.add(body, sensor_shape)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
        mouse_pos = pygame.mouse.get_pos()

        body.position = mouse_pos
        body.position -= pymunk.Vec2d(10, 50)
        body.angle = 1
        body.velocity = 0, 0
        body.angular_velocity = 0

        ### Update physics
        obj["last_set"] = None
        dt = 1.0 / 60.0

        space.step(dt)

        # point set

        # cpBool swapped = arb->swapped;
        # cpVect n = arb->n;
        # set.normal = (swapped ? cpvneg(n) : n);

        # for(int i=0; i<set.count; i++){
        #     // Contact points are relative to body CoGs;
        #     cpVect p1 = cpvadd(arb->body_a->p, arb->contacts[i].r1);
        #     cpVect p2 = cpvadd(arb->body_b->p, arb->contacts[i].r2);

        #     set.points[i].pointA = (swapped ? p2 : p1);
        #     set.points[i].pointB = (swapped ? p1 : p2);
        #     set.points[i].distance = cpvdot(cpvsub(p2, p1), n);
        # }

        # debug collision draw
        # cpSpaceDebugDrawSegmentImpl draw_seg = options->drawSegment;
        # cpDataPointer data = options->data;

        # for (int i = 0; i < arbiters->num; i++)
        # {
        # 	cpArbiter *arb = (cpArbiter *)arbiters->arr[i];
        # 	cpVect n = arb->n;

        # 	for (int j = 0; j < arb->count; j++)
        # 	{
        # 		cpVect p1 = cpvadd(arb->body_a->p, arb->contacts[j].r1);
        # 		cpVect p2 = cpvadd(arb->body_b->p, arb->contacts[j].r2);

        # 		cpFloat d = 2.0f;
        # 		cpVect a = cpvadd(p1, cpvmult(n, -d));
        # 		cpVect b = cpvadd(p2, cpvmult(n, d));

        # 		a = cpTransformPoint(options->transform, a);
        # 		b = cpTransformPoint(options->transform, b);
        # 		draw_seg(a, b, color, data);
        # 	}
        # }

        ### Draw stuff
        screen.fill(pygame.Color("white"))
        space.debug_draw(draw_options)
        if obj["last_set"] is not None:
            for point in obj["last_set"].points:

                n = obj["last_set"].normal
                # print(n, point.distance.get_distance())
                a = point.point_a + point.distance * n
                b = point.point_b  # - point.distance * n
                # print(point.distance, point.point_a.get_distance(point.point_b))
                # pygame.draw.circle(screen, pygame.Color("red"), a, 5)  # sensor
                pygame.draw.circle(screen, pygame.Color("blue"), b, 3)

        ### Flip screen
        pygame.display.flip()
        clock.tick(50)
        pygame.display.set_caption("fps: " + str(clock.get_fps()))


if __name__ == "__main__":

    main()
