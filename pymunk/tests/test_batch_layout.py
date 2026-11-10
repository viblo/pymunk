"""Check layout metadata against native packing and scalar body/arbiter data."""

import array
import itertools
import math
import unittest
from typing import Any, cast

import pymunk
from pymunk import batch


def selections(fields: Any) -> Any:
    members = list(fields)
    for selected in itertools.product((False, True), repeat=len(members)):
        flags = fields(0)
        for enabled, field in zip(selected, members):
            if enabled:
                flags |= field
        yield flags


def is_integer(field: Any) -> bool:
    return field in (
        batch.BodyFields.BODY_ID,
        batch.ArbiterFields.BODY_A_ID,
        batch.ArbiterFields.BODY_B_ID,
        batch.ArbiterFields.IS_FIRST_CONTACT,
        batch.ArbiterFields.CONTACT_COUNT,
    )


def strides(layout: Any) -> tuple[int, int]:
    return (
        sum(
            size
            for field, (offset, size) in layout.fields.items()
            if not is_integer(field)
        ),
        sum(
            size for field, (offset, size) in layout.fields.items() if is_integer(field)
        ),
    )


class UnitTestBatchLayout(unittest.TestCase):
    def test_layout_contract(self) -> None:
        F = batch.BodyFields
        flags = F.POSITION | F.ANGLE | F.BODY_ID
        layout = batch.get_body_layout(flags)
        self.assertIsInstance(layout, batch.Layout)
        self.assertEqual(list(layout.fields), [F.BODY_ID, F.ANGLE, F.POSITION])
        self.assertEqual(
            layout.fields, {F.BODY_ID: (0, 1), F.ANGLE: (0, 1), F.POSITION: (1, 2)}
        )
        self.assertEqual(strides(layout), (3, 1))
        with self.assertRaises(KeyError):
            layout[F.VELOCITY]
        with self.assertRaises(KeyError):
            layout[cast(Any, batch.ArbiterFields.BODY_A_ID)]
        # Mutable results are independent, including for repeated selections.
        layout.fields[F.ANGLE] = (99, 99)
        layout.fields.clear()
        self.assertEqual(batch.get_body_layout(flags)[F.ANGLE], (0, 1))
        af = batch.ArbiterFields
        arbiter_layout = batch.get_arbiter_layout(af.ALL)
        self.assertIsInstance(arbiter_layout, batch.Layout)
        arbiter_layout.fields.clear()
        self.assertEqual(batch.get_arbiter_layout(af.ALL)[af.BODY_A_ID], (0, 1))
        with self.assertRaises(TypeError):
            batch.get_body_layout(cast(Any, af.ALL))
        with self.assertRaises(TypeError):
            batch.get_arbiter_layout(cast(Any, F.ALL))
        with self.assertRaises(TypeError):
            batch.get_body_layout(cast(Any, 3))
        cases: tuple[tuple[Any, Any], ...] = (
            (F, batch.get_body_layout),
            (af, batch.get_arbiter_layout),
        )
        for enum, query in cases:
            self.assertEqual(query(enum(0)).fields, {})
            self.assertEqual(
                (query(enum(0)).float_stride, query(enum(0)).int_stride), (0, 0)
            )
            all_flags = enum(0)
            for field in enum:
                all_flags |= field
            self.assertEqual(query(enum.ALL).fields, query(all_flags).fields)
        self.assertEqual(F.BODY_ID.value, 1)
        self.assertEqual(F.POSITION.value, 2)
        self.assertEqual(F.ANGLE.value, 4)

    def test_component_views_and_validation(self) -> None:
        F = batch.BodyFields
        layout = batch.get_body_layout(F.BODY_ID | F.ANGLE | F.POSITION)
        source = array.array("d", [0.1, 10, 20, 0.2, 30, 40])
        values = memoryview(source)
        self.assertEqual(list(layout.component(values, F.ANGLE)), [0.1, 0.2])
        x = layout.component(values, F.POSITION, 0)
        y = layout.component(values, F.POSITION, 1)
        self.assertEqual(list(x), [10, 30])
        self.assertEqual(list(y), [20, 40])
        x[1] = 99
        self.assertEqual(source[4], 99)
        self.assertEqual(list(layout.component(values[:0], F.POSITION)), [])
        self.assertEqual(layout.component(list(source), F.POSITION, 1), [20, 40])
        for component in (-1, 2, 100):
            with self.assertRaises(IndexError):
                layout.component(values, F.POSITION, component)
        with self.assertRaises(IndexError):
            layout.component(values, F.ANGLE, 1)
        with self.assertRaises(TypeError):
            layout.component(values, F.POSITION, cast(Any, 0.5))
        with self.assertRaises(KeyError):
            layout.component(values, F.VELOCITY)
        ids = memoryview(array.array("I", [1, 2]))
        self.assertEqual(list(layout.component(ids, F.BODY_ID)), [1, 2])

    def test_component_integer_stride(self) -> None:
        F = batch.ArbiterFields
        layout = batch.get_arbiter_layout(
            F.BODY_A_ID | F.BODY_B_ID | F.TOTAL_IMPULSE | F.CONTACT_COUNT
        )
        self.assertEqual((layout.float_stride, layout.int_stride), (2, 3))
        self.assertEqual(layout.component([1, 2, 1, 3, 4, 2], F.BODY_A_ID), [1, 3])
        self.assertEqual(layout.component([1, 2, 1, 3, 4, 2], F.BODY_B_ID), [2, 4])
        self.assertEqual(layout.component([1, 2, 1, 3, 4, 2], F.CONTACT_COUNT), [1, 2])
        self.assertEqual(
            layout.component([10.0, 20.0, 30.0, 40.0], F.TOTAL_IMPULSE, 1), [20.0, 40.0]
        )

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

    def check_records(self, layout: Any, buffer: batch.Buffer, rows: Any) -> None:
        floats = memoryview(buffer.float_buf()).cast("d")
        ints = memoryview(buffer.int_buf()).cast("P")
        float_stride, int_stride = strides(layout)
        self.assertEqual(
            (layout.float_stride, layout.int_stride), (float_stride, int_stride)
        )
        self.assertEqual(len(floats), len(rows) * float_stride)
        self.assertEqual(len(ints), len(rows) * int_stride)
        for row, expected in enumerate(rows):
            for field, (offset, size) in layout.fields.items():
                integer = is_integer(field)
                values = ints if integer else floats
                stride = int_stride if integer else float_stride
                start = row * stride + offset
                actual = list(values[start : start + size])
                wanted = expected[field]
                for component in range(size):
                    view = layout.component(values, field, component)
                    self.assertEqual(
                        view.tobytes(), values[offset + component :: stride].tobytes()
                    )
                self.assertEqual(len(actual), len(wanted))
                for value, target in zip(actual, wanted):
                    if integer:
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
                float_stride, int_stride = strides(layout)
                values = array.array("d", [0.0] * (len(bodies) * float_stride))
                for row in range(len(bodies)):
                    for field, (offset, size) in layout.fields.items():
                        if field != F.BODY_ID:
                            assert isinstance(field, batch.BodyFields)
                            start = row * float_stride + offset
                            values[start : start + size] = array.array(
                                "d", targets[field]
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
                    float_stride, int_stride = strides(layout)
                    for field, (offset, size) in layout.fields.items():
                        integer = is_integer(field)
                        data = ints if integer else floats
                        stride = int_stride if integer else float_stride
                        start = record * stride + offset
                        row[field] = list(data[start : start + size])
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
