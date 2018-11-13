import unittest

import quadtree as sqt


class TestQuadtree(unittest.TestCase):
    def test_wrong_bbox(self):
        bbox = (10, 10, 0, 0)
        with self.assertRaises(ValueError) as raised:
            sqt.QuadTree(bbox)

        self.assertEqual(
            'Invalid bounding box: {}'.format(bbox),
            raised.exception.args[0])

    def test_empty(self):
        q = sqt.QuadTree((1, 1, 5, 5))
        self.assertEqual([], q.contents)
        self.assertEqual(tuple(), q.children)

    def test_simple_insert(self):
        q = sqt.QuadTree((0, 0, 10, 10))

        element = ("hello", 1, 1)

        insertion_outcome = q.insert(element)

        self.assertIs(True, insertion_outcome)
        self.assertIn(element, q)

    def test_out_of_bounds_element_not_inserted(self):
        q = sqt.QuadTree((0, 0, 1, 1))

        element = ("i should not be here", 10, 10)

        insertion_outcome = q.insert(element)

        self.assertIs(False, insertion_outcome)
        self.assertNotIn(element, q)

    def test_split_quadrants(self):
        q = sqt.QuadTree((0, 0, 4, 4), max_items=1)
        el1, el2 = ("el1", 1, 1), ("el2", 1, 3)

        i1 = q.insert(el1)
        i2 = q.insert(el2)

        self.assertIs(True, i1)
        self.assertIs(True, i2)

        self.assertIn(el1, q.children[0])
        self.assertIn(el2, q.children[3])

        self.assertIn(el1, q)
        self.assertIn(el2, q)

    def test_split_twice(self):
        q = sqt.QuadTree((0, 0, 10, 10), max_items=2)
        el1, el2, el3 = ("el1", 1, 2), ("el2", 7, 9), ("el3", 6, 3)
        el4, el5, el6 = ("el4", 8, 4), ("el5", 6, 2), ("el6", 6.5, 1.5)

        insert_outcomes = [q.insert(x) for x in (el1, el2, el3, el4, el5, el6)]

        not_inserted = ("not inserted", -1, -3)
        not_inserted_outcome = q.insert(not_inserted)

        self.assertTrue(all(insert_outcomes))
        self.assertFalse(not_inserted_outcome)

        self.assertIn(el1, q)
        self.assertIn(el2, q)
        self.assertIn(el3, q)
        self.assertIn(el4, q)
        self.assertIn(el5, q)
        self.assertIn(el6, q)
        self.assertNotIn(not_inserted, q)

        q1, q2, q3, q4 = q.children

        q2a, q2b, q2c, q2d = q2.children

        self.assertIn(el1, q1)
        self.assertIn(el2, q3)

        self.assertIn(el3, q2)
        self.assertIn(el4, q2)
        self.assertIn(el5, q2)
        self.assertIn(el6, q2)

        self.assertIn(el3, q2d)
        self.assertIn(el4, q2c)
        self.assertIn(el5, q2a)
        self.assertIn(el6, q2a)
        self.assertEqual([], q2b.contents)

        self.assertEqual([], q4.contents)

    def test_not_intersecting_bbox(self):
        q = sqt.QuadTree((0, 0, 10, 10))

        non_intersecting = (20, 20, 50, 50)

        self.assertEqual(set(), q.intersect(non_intersecting))

    def test_intersecting_bbox(self):
        q = sqt.QuadTree((0, 0, 10, 10))

        el1 = ("el1", 8.5, 9.5)
        el2 = ("el2", 1, 4)

        q.insert(el1)
        q.insert(el2)

        intersecting = (8, 9, 15, 15)

        self.assertEqual([el1, el2], q.contents)
        self.assertEqual(set([el1]), q.intersect(intersecting))

    def test_intersecting_bbox_with_simple_split(self):
        q = sqt.QuadTree((0, 0, 4, 4), max_items=1)
        el1, el2 = ("el1", 1, 1), ("el2", 1, 3)

        q.insert(el1)
        q.insert(el2)

        catch_both = (-1, -1, 2, 5)
        catch_el1 = (-1, 0.5, 1.5, 1.5)
        catch_el2 = (0, 2.5, 2, 4)

        [self.assertIn(el, q) for el in (el1, el2)]

        self.assertEqual(set([el1]), q.intersect(catch_el1))
        self.assertEqual(set([el2]), q.intersect(catch_el2))
        self.assertEqual(set([el1, el2]), q.intersect(catch_both))

    def test_intersecting_bbox_with_double_split(self):
        q = sqt.QuadTree((0, 0, 10, 10), max_items=2)
        el1, el2, el3 = ("el1", 1, 2), ("el2", 7, 9), ("el3", 6, 3)
        el4, el5, el6 = ("el4", 8, 4), ("el5", 6, 2), ("el6", 6.5, 1.5)

        all_elements = el1, el2, el3, el4, el5, el6

        catch_all = (-1, -1, 11, 11)
        catch_el3_el5_el6 = (4.5, -1, 7.3, 3.3)
        catch_el1_el5 = (0, 1.6, 10, 2.2)

        insert_outcomes = [q.insert(x) for x in all_elements]

        self.assertEqual(set(all_elements), q.intersect(catch_all))
        self.assertEqual(set([el3, el5, el6]), q.intersect(catch_el3_el5_el6))
        self.assertEqual(set([el1, el5]), q.intersect(catch_el1_el5))

        self.assertTrue(all(insert_outcomes))

    def test_dont_split_if_max_depth0_is_reached(self):
        q = sqt.QuadTree((0, 0, 10, 10), max_items=2, max_depth=0)
        elements = el1, el2, el3 = ("el1", 1, 2), ("el2", 7, 9), ("el3", 6, 3)
        insert_outcomes = [q.insert(x) for x in elements]

        self.assertEqual(list(elements), q.contents)
        self.assertTrue(all(insert_outcomes))

    def test_dont_split_if_max_depth1_is_reached(self):
        q = sqt.QuadTree((0, 0, 10, 10), max_items=2, max_depth=1)
        elements = el1, el2, el3, el4 = ("el1", 1, 2), ("el2", 7, 9), ("el3", 6, 3), ("el4", 8, 4)

        insert_outcomes = [q.insert(x) for x in elements]

        q1, q2, q3, q4 = q.children

        self.assertEqual([], q.contents)
        self.assertEqual([el1], q1.contents)
        self.assertEqual([el3, el4], q2.contents)
        self.assertEqual([el2], q3.contents)
        self.assertEqual([], q4.contents)
        self.assertTrue(all(insert_outcomes))

    def test_lookup_value(self):
        q = sqt.QuadTree((0, 0, 10, 10))

        element = ("hello", 1, 1)
        element_same_value = ("hello", 2, 2)

        q.insert(element)
        q.insert(element_same_value)

        self.assertEqual(element, q[element[0]])

    def test_iter(self):
        q = sqt.QuadTree((0, 0, 5, 5), max_items=2, max_depth=2)
        self.assertSetEqual(set(), {x for x in q})

        e1 = ("hello1", 1, 1)
        q.insert(e1)
        self.assertSetEqual({e1}, {x for x in q})

        e2 = ("hello2", 2, 2)
        q.insert(e2)
        self.assertSetEqual({e1, e2}, {x for x in q})

        # split
        e3 = ("hello3", 0, 1)
        q.insert(e3)
        self.assertSetEqual({e1, e2, e3}, {x for x in q})

    def test_lookup_absent_value(self):
        q = sqt.QuadTree((0, 0, 10, 10))

        element = ("hello", 1, 1)

        q.insert(element)

        with self.assertRaises(KeyError) as raised:
            q['absent']

        self.assertEqual('absent', raised.exception.args[0])

    def test_lookup_value_with_split(self):
        q = sqt.QuadTree((0, 0, 10, 10), max_items=2)
        el1, el2, el3 = ("el1", 1, 2), ("el2", 7, 9), ("el3", 6, 3)
        el4, el5, el6 = ("el4", 8, 4), ("el5", 6, 2), ("el6", 6.5, 1.5)

        all_elements = el1, el2, el3, el4, el5, el6

        [q.insert(x) for x in all_elements]

        self.assertEqual(el1, q[el1[0]])

    def test_lookup_absent_value_with_split(self):
        q = sqt.QuadTree((0, 0, 10, 10), max_items=2)
        el1, el2, el3 = ("el1", 1, 2), ("el2", 7, 9), ("el3", 6, 3)
        el4, el5, el6 = ("el4", 8, 4), ("el5", 6, 2), ("el6", 6.5, 1.5)

        all_elements = el1, el2, el3, el4, el5, el6

        [q.insert(x) for x in all_elements]

        with self.assertRaises(KeyError) as raised:
            q['absent']

        self.assertEqual('absent', raised.exception.args[0])

    def test_repr(self):
        q = sqt.QuadTree((0, 0, 10, 10), max_items=2, max_depth=8)
        self.assertEqual('QuadTree((0, 0, 10, 10), 2, 8)', repr(q))


if __name__ == '__main__':
    unittest.main()
