import unittest
import sys
sys.path.append(r"battlesnake/components")
from snake import Snake
from coordinate import Coordinate
# from components.snake import Snake
# from components.coordinate import Coordinate

class TestSnake(unittest.TestCase):

    def setUp(self):
        snake_json = {
            'id': '123',
            'name': 'TestSnake',
            'health': 100,
            'body': [{'x': 2, 'y': 2}, {'x': 2, 'y': 3}, {'x': 2, 'y': 4}],
            'latency': 0,
            'shout': 'Hello!',
            'squad': 'Team A',
            'customizations': []
        }
        self.snake = Snake(snake_json)

    def test_safe_moves(self):
        safe_moves = self.snake.safe_moves()
        # self.assertEqual(3, len(safe_moves))

    def test_move(self):
        foods = [{'x': 1, 'y': 2}, {'x': 3, 'y': 3}]
        up_snake = self.snake.move(foods, 'up')
        self.assertEqual(self.snake.length, up_snake.length)
        
        left_snake = self.snake.move(foods, 'left')
        self.assertEqual(self.snake.length + 1, left_snake.length)

    def test_permute(self):
        foods = [{'x': 2, 'y': 2}, {'x': 3, 'y': 3}]
        permutations = self.snake.permute(foods)
        # self.assertEqual(3, len(permutations))

    def test_get_json(self):
        snake_data = self.snake.get_json()
        self.assertEqual('123', snake_data['id'])
        self.assertEqual('TestSnake', snake_data['name'])


if __name__ == '__main__':
    unittest.main()
