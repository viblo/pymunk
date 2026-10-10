import copy
import pickle
import unittest
from typing import Any

import pymunk as p


def record_data(arbiter: p.Arbiter, space: p.Space, data: Any) -> None:
    getattr(space, "observed").append(data)


def clone(space: p.Space, method: str) -> p.Space:
    if method == "pickle":
        return pickle.loads(pickle.dumps(space))
    if method == "deepcopy":
        return copy.deepcopy(space)
    return space.copy()


def make_space() -> p.Space:
    space = p.Space()
    setattr(space, "observed", [])
    body = p.Body(1, 1)
    shape = p.Circle(body, 1)
    shape.collision_type = 1
    floor = p.Circle(space.static_body, 1)
    floor.collision_type = 2
    space.add(body, shape, floor)
    return space


class UnitTestCollisionDataCopy(unittest.TestCase):
    def test_each_phase_keeps_its_data(self) -> None:
        for method in ["copy", "deepcopy", "pickle"]:
            for types in [(None, None), (1, None), (1, 2)]:
                with self.subTest(method=method, types=types):
                    space = make_space()
                    space.on_collision(
                        *types, begin=record_data, data={"phase": "begin"}
                    )
                    space.on_collision(
                        *types, pre_solve=record_data, data={"phase": "pre"}
                    )
                    space.on_collision(
                        *types, post_solve=record_data, data={"phase": "post"}
                    )
                    space.on_collision(
                        *types, separate=record_data, data={"phase": "separate"}
                    )
                    restored = clone(space, method)
                    restored.step(0.01)
                    restored.remove(next(iter(restored.shapes)))
                    self.assertEqual(
                        getattr(restored, "observed"),
                        [
                            {"phase": "begin"},
                            {"phase": "pre"},
                            {"phase": "post"},
                            {"phase": "separate"},
                        ],
                    )
                    self.assertEqual(getattr(space, "observed"), [])

    def test_shared_data_references_are_copied_together(self) -> None:
        for method in ["copy", "deepcopy", "pickle"]:
            with self.subTest(method=method):
                space = make_space()
                data = {"body": next(iter(space.bodies)), "values": [1]}
                setattr(space, "game_data", data)
                space.on_collision(begin=record_data, pre_solve=record_data, data=data)
                restored = clone(space, method)
                restored.step(0.01)
                seen = getattr(restored, "observed")
                self.assertEqual(len(seen), 2)
                self.assertIs(seen[0], seen[1])
                self.assertIs(seen[0], getattr(restored, "game_data"))
                self.assertIs(seen[0]["body"], next(iter(restored.bodies)))
                self.assertIsNot(seen[0], data)
                seen[0]["values"].append(2)
                self.assertEqual(data["values"], [1])

    def test_state_without_handler_data(self) -> None:
        space = make_space()
        space.on_collision(begin=record_data)
        state = copy.deepcopy(space.__getstate__())
        for name, handlers in state["special"]:
            if name == "_handlers":
                for _, handler in handlers:
                    handler.pop("_data", None)
        restored = p.Space.__new__(p.Space)
        restored.__setstate__(state)
        restored.step(0.01)
        self.assertEqual(getattr(restored, "observed"), [None])
