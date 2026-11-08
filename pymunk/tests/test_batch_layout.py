"""Check layout metadata against native packing and scalar body/arbiter data."""

import array
import dataclasses
import itertools
import math
import unittest
from typing import Any, cast

import pymunk
from pymunk import batch
from pymunk._chipmunk_cffi import ffi


def selections(fields: Any) -> Any:
    members = list(fields)
    for selected in itertools.product((False, True), repeat=len(members)):
        flags = fields(0)
        for enabled, field in zip(selected, members):
            if enabled:
                flags |= field
        yield flags


class UnitTestBatchLayout(unittest.TestCase):
    def test_layout_contract(self) -> None:
        F = batch.BodyFields
        layout = batch.get_body_layout(F.POSITION | F.ANGLE | F.BODY_ID)
        self.assertEqual(
            [e.field for e in layout.fields], [F.BODY_ID, F.ANGLE, F.POSITION]
        )
        self.assertEqual(layout[F.BODY_ID], batch.FieldLayout(F.BODY_ID, "int", 0, 1))
        self.assertEqual(layout[F.ANGLE], batch.FieldLayout(F.ANGLE, "float", 0, 1))
        self.assertEqual(
            layout[F.POSITION], batch.FieldLayout(F.POSITION, "float", 1, 2)
        )
        self.assertEqual((layout.float_stride, layout.int_stride), (3, 1))
        self.assertEqual(layout.float_itemsize, ffi.sizeof("cpFloat"))
        self.assertEqual(layout.int_itemsize, ffi.sizeof("uintptr_t"))
        self.assertIs(layout, batch.get_body_layout(F.POSITION | F.ANGLE | F.BODY_ID))
        with self.assertRaises(KeyError):
            layout[F.VELOCITY]
        with self.assertRaises(KeyError):
            layout[batch.ArbiterFields.BODY_A_ID]
        with self.assertRaises(dataclasses.FrozenInstanceError):
            setattr(layout, "float_stride", 0)
        with self.assertRaises(dataclasses.FrozenInstanceError):
            setattr(layout[F.POSITION], "offset", 0)
        with self.assertRaises(TypeError):
            batch.get_body_layout(cast(Any, batch.ArbiterFields.ALL))
        with self.assertRaises(TypeError):
            batch.get_arbiter_layout(cast(Any, F.ALL))
        with self.assertRaises(TypeError):
            batch.get_body_layout(cast(Any, 3))
        cases: tuple[tuple[Any, Any], ...] = (
            (F, batch.get_body_layout),
            (batch.ArbiterFields, batch.get_arbiter_layout),
        )
        for enum, query in cases:
            empty = query(enum(0))
            self.assertEqual(empty.fields, ())
            self.assertEqual((empty.float_stride, empty.int_stride), (0, 0))
            all_flags = enum(0)
            for field in enum:
                all_flags |= field
            self.assertEqual(query(enum.ALL), query(all_flags))
        # Changing packing order must not change numeric masks.
        self.assertEqual(F.BODY_ID.value, 1)
        self.assertEqual(F.POSITION.value, 2)
        self.assertEqual(F.ANGLE.value, 4)

    def test_body_get_all_subsets(self) -> None:
        F = batch.BodyFields
        space = pymunk.Space()
        bodies = []
        expected = {}
        for i in range(3):
            body = pymunk.Body(1, 2)
            body.center_of_gravity = (2, -1)
            body.angle = 0.25 + i
            body.position = (10 + i, 20 + i)
            body.velocity = (30 + i, 40 + i)
            body.angular_velocity = 50 + i
            body.force = (60 + i, 70 + i)
            body.torque = 80 + i
            space.add(body)
            bodies.append(body)
            expected[body.id] = {
                F.BODY_ID: [body.id],
                F.ANGLE: [body.angle],
                F.POSITION: list(body.position),
                F.VELOCITY: list(body.velocity),
                F.ANGULAR_VELOCITY: [body.angular_velocity],
                F.FORCE: list(body.force),
                F.TORQUE: [body.torque],
            }
        ids = batch.Buffer()
        batch.get_space_bodies(space, F.BODY_ID, ids)
        order = list(memoryview(ids.int_buf()).cast("P"))
        buffer = batch.Buffer()
        for flags in selections(F):
            with self.subTest(flags=flags):
                buffer.clear()
                batch.get_space_bodies(space, flags, buffer)
                self.check_records(
                    batch.get_body_layout(flags), buffer, [expected[i] for i in order]
                )

    def check_records(
        self, layout: batch.Layout, buffer: batch.Buffer, rows: Any
    ) -> None:
        floats = memoryview(buffer.float_buf()).cast("d")
        ints = memoryview(buffer.int_buf()).cast("P")
        self.assertEqual(len(floats), len(rows) * layout.float_stride)
        self.assertEqual(len(ints), len(rows) * layout.int_stride)
        for row, expected in enumerate(rows):
            for entry in layout.fields:
                values = floats if entry.buffer == "float" else ints
                stride = (
                    layout.float_stride
                    if entry.buffer == "float"
                    else layout.int_stride
                )
                start = row * stride + entry.offset
                actual = list(values[start : start + entry.size])
                wanted = expected[entry.field]
                self.assertEqual(len(actual), len(wanted))
                for value, target in zip(actual, wanted):
                    if entry.buffer == "int":
                        self.assertEqual(value, target)
                    elif math.isnan(target):
                        # TOTAL_KE can already be NaN in scalar arbiter data.
                        self.assertTrue(math.isnan(value))
                    else:
                        self.assertAlmostEqual(value, target, places=10)

    def test_body_set_all_subsets(self) -> None:
        F = batch.BodyFields
        targets = {
            F.ANGLE: [1.2],
            F.POSITION: [7.0, 8.0],
            F.VELOCITY: [2.0, 3.0],
            F.ANGULAR_VELOCITY: [4.0],
            F.FORCE: [5.0, 6.0],
            F.TORQUE: [9.0],
        }
        for flags in selections(F):
            with self.subTest(flags=flags):
                space = pymunk.Space()
                bodies = [pymunk.Body(1, 2), pymunk.Body(2, 3)]
                for body in bodies:
                    body.center_of_gravity = (2, -1)
                    body.angle = 0.3
                    body.position = (0, 0)
                    space.add(body)
                layout = batch.get_body_layout(flags)
                values = array.array("d", [0.0] * (len(bodies) * layout.float_stride))
                for row in range(len(bodies)):
                    for entry in layout.fields:
                        if entry.buffer == "float":
                            assert isinstance(entry.field, batch.BodyFields)
                            start = row * layout.float_stride + entry.offset
                            values[start : start + entry.size] = array.array(
                                "d", targets[entry.field]
                            )
                buffer = batch.Buffer()
                buffer.set_float_buf(values)
                before = bytes(buffer.float_buf())
                batch.set_space_bodies(space, flags, buffer)
                self.assertEqual(bytes(buffer.float_buf()), before)
                for body in bodies:
                    scalar = pymunk.Body(body.mass, body.moment)
                    scalar.center_of_gravity = body.center_of_gravity
                    scalar.angle = 0.3
                    scalar.position = (0, 0)
                    for field, name in (
                        (F.ANGLE, "angle"),
                        (F.POSITION, "position"),
                        (F.VELOCITY, "velocity"),
                        (F.ANGULAR_VELOCITY, "angular_velocity"),
                        (F.FORCE, "force"),
                        (F.TORQUE, "torque"),
                    ):
                        if field in flags:
                            value = targets[field]
                            setattr(
                                scalar, name, value if len(value) == 2 else value[0]
                            )
                        self.assertEqual(getattr(body, name), getattr(scalar, name))
                # ID selection needs no integer input: the setter ignores it.
                self.assertEqual(len(memoryview(buffer.int_buf())), 0)

    def test_arbiter_get_all_subsets(self) -> None:
        F = batch.ArbiterFields
        for contacts in (0, 1, 2):
            space = pymunk.Space()
            a = pymunk.Body(1, 10)
            b = pymunk.Body(1, 10)
            b.position = (1.5, 0)
            a.velocity = (1, 0.2)
            b.velocity = (-1, -0.1)
            sa: pymunk.Shape
            sb: pymunk.Shape
            if contacts == 2:
                sa = pymunk.Poly.create_box(a, (2, 2))
                sb = pymunk.Poly.create_box(b, (2, 2))
            else:
                sa = pymunk.Circle(a, 1)
                sb = pymunk.Circle(b, 1)
                sa.sensor = contacts == 0
            space.add(a, b, sa, sb)
            c = pymunk.Body(1, 10)
            d = pymunk.Body(1, 10)
            c.position = (10, 0)
            d.position = (11.5, 0)
            sc: pymunk.Shape
            sd: pymunk.Shape
            if contacts == 2:
                sc = pymunk.Poly.create_box(c, (2, 2))
                sd = pymunk.Poly.create_box(d, (2, 2))
            else:
                sc = pymunk.Circle(c, 1)
                sd = pymunk.Circle(d, 1)
                sc.sensor = contacts == 0
            space.add(c, d, sc, sd)
            space.step(0.01)
            # Scalar views are mirrored by each_arbiter. Use the orientation
            # of the native cached-arbiter iteration, obtained from the IDs.
            snapshots: dict[tuple[int, int], Any] = {}

            def snapshot(arb: pymunk.Arbiter) -> None:
                aa, bb = arb.shapes
                assert aa.body is not None and bb.body is not None
                points = arb.contact_point_set.points
                self.assertEqual(len(points), contacts)
                row = {
                    F.BODY_A_ID: [aa.body.id],
                    F.BODY_B_ID: [bb.body.id],
                    F.TOTAL_IMPULSE: list(arb.total_impulse),
                    F.TOTAL_KE: [arb.total_ke],
                    F.IS_FIRST_CONTACT: [int(arb.is_first_contact)],
                    F.NORMAL: list(arb.normal),
                    F.CONTACT_COUNT: [len(points)],
                }
                for i, (fa, fb, fd) in enumerate(
                    (
                        (F.POINT_A_1, F.POINT_B_1, F.DISTANCE_1),
                        (F.POINT_A_2, F.POINT_B_2, F.DISTANCE_2),
                    )
                ):
                    row[fa] = list(points[i].point_a) if i < len(points) else [0.0, 0.0]
                    row[fb] = list(points[i].point_b) if i < len(points) else [0.0, 0.0]
                    row[fd] = [points[i].distance] if i < len(points) else [0.0]
                snapshots[(aa.body.id, bb.body.id)] = row

            a.each_arbiter(snapshot)
            b.each_arbiter(snapshot)
            c.each_arbiter(snapshot)
            d.each_arbiter(snapshot)
            ids = batch.Buffer()
            batch.get_space_arbiters(space, F.BODY_A_ID | F.BODY_B_ID, ids)
            order = list(memoryview(ids.int_buf()).cast("P"))
            # Sensors have no each_arbiter entries; take their non-contact
            # fields directly from an independent full native record instead.
            if contacts == 0:
                full = batch.Buffer()
                batch.get_space_arbiters(space, F.ALL, full)
                layout = batch.get_arbiter_layout(F.ALL)
                floats = memoryview(full.float_buf()).cast("d")
                ints = memoryview(full.int_buf()).cast("P")
                for record in range(len(order) // 2):
                    row = {}
                    for entry in layout.fields:
                        assert isinstance(entry.field, batch.ArbiterFields)
                        data = floats if entry.buffer == "float" else ints
                        stride = (
                            layout.float_stride
                            if entry.buffer == "float"
                            else layout.int_stride
                        )
                        start = record * stride + entry.offset
                        row[entry.field] = list(data[start : start + entry.size])
                    self.assertEqual(row[F.CONTACT_COUNT], [0])
                    for field in (F.POINT_A_1, F.POINT_B_1, F.POINT_A_2, F.POINT_B_2):
                        self.assertEqual(row[field], [0.0, 0.0])
                    self.assertEqual(row[F.DISTANCE_1], [0.0])
                    self.assertEqual(row[F.DISTANCE_2], [0.0])
                    snapshots[(order[record * 2], order[record * 2 + 1])] = row
            self.assertEqual(len(order), 4)
            rows = [
                snapshots[(order[i], order[i + 1])] for i in range(0, len(order), 2)
            ]
            buffer = batch.Buffer()
            for flags in selections(F):
                with self.subTest(contacts=contacts, flags=flags):
                    buffer.clear()
                    batch.get_space_arbiters(space, flags, buffer)
                    self.check_records(batch.get_arbiter_layout(flags), buffer, rows)
