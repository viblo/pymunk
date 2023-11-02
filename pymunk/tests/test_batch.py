import unittest

import pymunk
import pymunk.batch


class UnitTestBatch(unittest.TestCase):
    def test_empty(self) -> None:
        s = pymunk.Space()

        data = pymunk.batch.Buffer()
        pymunk.batch.get_space_bodies(s, pymunk.batch.BodyFields.BODY_ID, data)

        self.assertEqual(list(memoryview(data.float_buf()).cast("d")), [])
        self.assertEqual(list(memoryview(data.int_buf()).cast("P")), [])

        data = pymunk.batch.Buffer()
        pymunk.batch.get_space_arbiters(s, pymunk.batch.ArbiterFields.BODY_A_ID, data)

        self.assertEqual(list(memoryview(data.float_buf()).cast("d")), [])
        self.assertEqual(list(memoryview(data.int_buf()).cast("P")), [])

    def test_get_bodies(self) -> None:
        s = pymunk.Space()

        b1 = pymunk.Body(1, 1)
        b1.position = 1, 2
        b1.velocity = 3, 4
        b1.angle = 0.1
        b1.angular_velocity = 5
        s.add(b1, pymunk.Circle(b1, 4))

        b2 = pymunk.Body(1, 1)
        b2.position = 11, 12
        b2.velocity = 13, 14
        b2.angle = 0.11
        b2.angular_velocity = 15
        s.add(b2, pymunk.Circle(b2, 4))

        data = pymunk.batch.Buffer()

        pymunk.batch.get_space_bodies(
            s, pymunk.batch.BodyFields.BODY_ID | pymunk.batch.BodyFields.POSITION, data
        )

        self.assertEqual(
            list(memoryview(data.float_buf()).cast("d")), [1.0, 2.0, 11.0, 12.0]
        )
        self.assertEqual(list(memoryview(data.int_buf()).cast("P")), [b1.id, b2.id])

        data = pymunk.batch.Buffer()
        pymunk.batch.get_space_bodies(s, pymunk.batch.BodyFields.ALL, data)

        self.assertEqual(
            list(memoryview(data.float_buf()).cast("d")),
            [1.0, 2.0, 0.1, 3.0, 4.0, 5.0, 11.0, 12.0, 0.11, 13.0, 14.0, 15.0],
        )
        self.assertEqual(list(memoryview(data.int_buf()).cast("P")), [b1.id, b2.id])

    def test_get_arbiters(self) -> None:
        s = pymunk.Space()

        b1 = pymunk.Body(1, 1)
        b1.position = 1, 2
        b1.velocity = (1, 0)
        s1 = pymunk.Circle(b1, 40)
        s.add(b1, s1)

        b2 = pymunk.Body(1, 1)
        b2.position = 11, 12
        s2 = pymunk.Poly.create_box(b2)
        s.add(b2, s2)

        b3 = pymunk.Body(1, 1)
        b3.position = 21, 22
        b3.velocity = (-1, 0)
        s3 = pymunk.Poly.create_box(b3)
        s.add(b3, s3)

        s.step(0.1)

        data = pymunk.batch.Buffer()
        pymunk.batch.get_space_arbiters(
            s,
            pymunk.batch.ArbiterFields.BODY_A_ID | pymunk.batch.ArbiterFields.BODY_B_ID,
            data,
        )

        self.assertEqual(list(memoryview(data.float_buf()).cast("d")), [])

        actual_ids = sorted(memoryview(data.int_buf()).cast("P"))
        expected_ids = sorted([b1.id, b1.id, b2.id, b2.id, b3.id, b3.id])
        self.assertSequenceEqual(actual_ids, expected_ids)

        data.clear()

        pymunk.batch.get_space_arbiters(s, pymunk.batch.ArbiterFields.ALL, data)

        floats = memoryview(data.float_buf()).cast("d")
        ints = memoryview(data.int_buf()).cast("P")

        def check_arb_data(arb: pymunk.Arbiter) -> None:
            a_id = arb.shapes[0].body.id
            b_id = arb.shapes[1].body.id

            if a_id == ints[0] and b_id == ints[1]:
                idx = 0
            elif a_id == ints[4] and b_id == ints[5]:
                idx = 1
            elif a_id == ints[8] and b_id == ints[9]:
                idx = 2
            else:
                # When using each_arbiter a mirror of each arbiter will be
                # returned as well. These we ignore.
                return
            # print(a_id, b_id, idx, arb.total_impulse)
            # Assert int values
            self.assertEqual(arb.is_first_contact, ints[idx * 4 + 2])
            self.assertEqual(len(arb.contact_point_set.points), ints[idx * 4 + 3])

            # Assert floats
            o = len(floats) // 3
            points = arb.contact_point_set.points
            self.assertEqual(arb.total_impulse.x, floats[(idx * o + 0)])
            self.assertEqual(arb.total_impulse.y, floats[(idx * o + 1)])
            self.assertEqual(arb.total_ke, floats[(idx * o + 2)])
            self.assertEqual(arb.normal.x, floats[(idx * o + 3)])
            self.assertEqual(arb.normal.y, floats[(idx * o + 4)])
            self.assertEqual(points[0].point_a.x, floats[(idx * o + 5)])
            self.assertEqual(points[0].point_a.y, floats[(idx * o + 6)])
            self.assertEqual(points[0].point_b.x, floats[(idx * o + 7)])
            self.assertEqual(points[0].point_b.y, floats[(idx * o + 8)])
            self.assertEqual(points[0].distance, floats[(idx * o + 9)])
            if len(points) == 2:
                self.assertEqual(points[1].point_a.x, floats[(idx * o + 10)])
                self.assertEqual(points[1].point_a.y, floats[(idx * o + 11)])
                self.assertEqual(points[1].point_b.x, floats[(idx * o + 12)])
                self.assertEqual(points[1].point_b.y, floats[(idx * o + 13)])
                self.assertEqual(points[1].distance, floats[(idx * o + 14)])
            else:
                self.assertEqual(0, floats[(idx * o + 10)])
                self.assertEqual(0, floats[(idx * o + 11)])
                self.assertEqual(0, floats[(idx * o + 12)])
                self.assertEqual(0, floats[(idx * o + 13)])
                self.assertEqual(0, floats[(idx * o + 14)])

        b1.each_arbiter(check_arb_data)
        b2.each_arbiter(check_arb_data)
        b3.each_arbiter(check_arb_data)
