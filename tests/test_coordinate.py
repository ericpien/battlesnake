import unittest
import sys
sys.path.append(r"battlesnake/components")
from coordinate import Coordinate

class TestCoordinate(unittest.TestCase):

    def test_add(self):
        coord1 = Coordinate({'x': 1, 'y': 2})
        coord2 = Coordinate({'x': 3, 'y': 4})
        result = coord1 + coord2
        self.assertEqual(result.x, 4)
        self.assertEqual(result.y, 6)

    def test_equality(self):
        coord1 = Coordinate({'x': 1, 'y': 2})
        coord2 = Coordinate({'x': 1, 'y': 2})
        self.assertEqual(coord1, coord2)

    def test_move_left(self):
        coord = Coordinate({'x': 2, 'y': 3})
        new_coord = coord.move_left()
        self.assertEqual(new_coord.x, 1)
        self.assertEqual(new_coord.y, 3)

    def test_move_right(self):
        coord = Coordinate({'x': 2, 'y': 3})
        new_coord = coord.move_right()
        self.assertEqual(new_coord.x, 3)
        self.assertEqual(new_coord.y, 3)

if __name__ == '__main__':
    unittest.main()