import copy
import pickle
import unittest

import pymunk as p


def custom_position(body: p.Body, dt: float) -> None:
    body.position += 100, 0


def custom_velocity(
    body: p.Body, gravity: tuple[float, float], damping: float, dt: float
) -> None:
    body.velocity = 100, 0


class UnitTestResetIntegrators(unittest.TestCase):
    def test_reset_callback_getters(self) -> None:
        body = p.Body(1, 1)
        body.position_func = custom_position
        body.velocity_func = custom_velocity
        body.position_func = p.Body.update_position
        body.velocity_func = p.Body.update_velocity
        self.assertEqual(body.position_func, p.Body.update_position)
        self.assertEqual(body.velocity_func, p.Body.update_velocity)

    def test_reset_callbacks_stay_reset_after_copy(self) -> None:
        for kind in ["position", "velocity"]:
            for method in ["copy", "deepcopy", "pickle"]:
                with self.subTest(kind=kind, method=method):
                    space = p.Space()
                    space.gravity = 0, -10
                    body = p.Body(1, 1)
                    body.velocity = 2, 0
                    space.add(body)
                    if kind == "position":
                        body.position_func = custom_position
                        body.position_func = p.Body.update_position
                    else:
                        body.velocity_func = custom_velocity
                        body.velocity_func = p.Body.update_velocity
                    if method == "copy":
                        restored = space.copy()
                    elif method == "deepcopy":
                        restored = copy.deepcopy(space)
                    else:
                        restored = pickle.loads(pickle.dumps(space))
                    restored_body = next(iter(restored.bodies))
                    for _ in range(10):
                        space.step(0.1)
                        restored.step(0.1)
                        self.assertEqual(restored_body.position, body.position)
                        self.assertEqual(restored_body.velocity, body.velocity)

    def test_custom_callbacks_can_be_reinstalled(self) -> None:
        space = p.Space()
        body = p.Body(1, 1)
        space.add(body)
        body.position_func = custom_position
        body.velocity_func = custom_velocity
        body.position_func = p.Body.update_position
        body.velocity_func = p.Body.update_velocity
        body.position_func = custom_position
        body.velocity_func = custom_velocity
        restored = space.copy()
        restored.step(0.1)
        restored_body = next(iter(restored.bodies))
        self.assertEqual(restored_body.position, (100, 0))
        self.assertEqual(restored_body.velocity, (100, 0))
