"""Installed-wheel browser checks; executed by test_pyodide_wheels.mjs."""

import json
import math
import pickle
import struct
import sys

import pymunk
import pymunk.tests
from pymunk._chipmunk_cffi import lib

assert sys.platform == "emscripten"
assert not lib.cpContactSolverIsAvailable(lib.CP_CONTACT_SOLVER_AVX2)
assert lib.cpContactSolverIsAvailable(lib.CP_CONTACT_SOLVER_WASM_SIMD)
assert pymunk.tests.run_tests(filter="test"), "Pymunk's installed test suite failed"


def post_solve(arbiter, space, data):
    data["calls"] += 1
    try:
        space.solver_mode = pymunk.SolverMode.DEFAULT
    except AssertionError:
        data["locked"] += 1
    else:
        data["errors"] += 1


def make_joint(kind, a, b):
    distance = a.position.get_distance(b.position)
    if kind == 0:
        return pymunk.PinJoint(a, b)
    if kind == 1:
        return pymunk.SlideJoint(a, b, (0, 0), (0, 0), distance * 0.9, distance * 1.1)
    if kind == 2:
        return pymunk.PivotJoint(a, b, (a.position + b.position) / 2)
    if kind == 3:
        return pymunk.GrooveJoint(a, b, (0, -0.3), (distance + 0.3, 0), (0, 0))
    if kind == 4:
        return pymunk.GearJoint(a, b, 0, 1)
    if kind == 5:
        return pymunk.RatchetJoint(a, b, 0, 0.25)
    if kind == 6:
        return pymunk.RotaryLimitJoint(a, b, -0.4, 0.4)
    if kind == 7:
        return pymunk.DampedSpring(a, b, (0, 0), (0, 0), distance, 30, 2)
    if kind == 8:
        return pymunk.DampedRotarySpring(a, b, 0, 10, 2)
    return pymunk.SimpleMotor(a, b, 0.25)


def make_world(kind, mode):
    space = pymunk.Space()
    assert space.solver_mode == pymunk.SolverMode.DEFAULT
    assert lib.cpSpaceGetContactSolver(space._space) == lib.CP_CONTACT_SOLVER_ORIGINAL
    space.solver_mode = mode
    expected = (lib.CP_CONTACT_SOLVER_WASM_SIMD if mode == pymunk.SolverMode.AUTO
                else lib.CP_CONTACT_SOLVER_ORIGINAL)
    assert lib.cpSpaceGetContactSolver(space._space) == expected
    space.gravity = (0, -10)
    space.collision_slop = 0.005
    floor = pymunk.Segment(space.static_body, (-100, 0), (100, 0), 0)
    floor.friction = 1
    space.add(floor)
    bodies = []
    for i in range(16):
        body = pymunk.Body(1, pymunk.moment_for_box(1, (1, 1)))
        body.position = (-23 + i * 2, 0.45)
        body.velocity = ((i % 3 - 1) * 0.1, 0)
        shape = pymunk.Poly.create_box(body, (1, 1))
        shape.friction = 0.7
        space.add(body, shape)
        bodies.append(body)
    joints = []
    for i in range(0, len(bodies), 2):
        joint = make_joint(kind, bodies[i], bodies[i + 1])
        joint.max_force = 50
        space.add(joint)
        joints.append(joint)
    data = dict(calls=0, locked=0, errors=0)
    space.on_collision(None, None, post_solve=post_solve, data=data)
    return space, bodies, joints, data


callback_calls = 0
for kind in range(10):
    original = make_world(kind, pymunk.SolverMode.DEFAULT)
    accelerated = make_world(kind, pymunk.SolverMode.AUTO)
    for step in range(120):
        for space, bodies, joints, data in (original, accelerated):
            space.iterations = (1, 10, 20)[step % 3]
            space.step(1 / 60 if step % 2 else 1 / 120)
        for a, b in zip(original[1], accelerated[1]):
            x = (*a.position, *a.velocity, a.angle, a.angular_velocity)
            y = (*b.position, *b.velocity, b.angle, b.angular_velocity)
            assert all(math.isfinite(v) for v in (*x, *y))
            assert struct.pack("6d", *x) == struct.pack("6d", *y)
        for a, b in zip(original[2], accelerated[2]):
            assert struct.pack("d", a.impulse) == struct.pack("d", b.impulse)
    for data in (original[3], accelerated[3]):
        assert data["calls"] > 0 and data["calls"] == data["locked"]
        assert data["errors"] == 0
        callback_calls += data["calls"]

space = accelerated[0]
for clone in (space.copy(), pickle.loads(pickle.dumps(space))):
    assert clone.solver_mode == pymunk.SolverMode.AUTO
    assert lib.cpSpaceGetContactSolver(clone._space) == lib.CP_CONTACT_SOLVER_WASM_SIMD
    clone.step(1 / 60)
space.solver_mode = pymunk.SolverMode.DEFAULT
assert lib.cpSpaceGetContactSolver(space._space) == lib.CP_CONTACT_SOLVER_ORIGINAL
space.solver_mode = pymunk.SolverMode.AUTO
assert lib.cpSpaceGetContactSolver(space._space) == lib.CP_CONTACT_SOLVER_WASM_SIMD

json.dumps(dict(
    python=sys.version,
    pymunk=pymunk.version,
    engine=pymunk.chipmunk_version,
    installed_tests=True,
    selected=int(lib.cpSpaceGetContactSolver(space._space)),
    joint_types=10,
    paired_mixed_steps=1200,
    callback_calls=callback_calls,
    original_exact=True,
    copy_pickle=True,
    default_unchanged=True,
))
