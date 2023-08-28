import unittest
import sys
sys.path.append(r"battlesnake/components")
from board import Board
from snake import Snake
from coordinate import Coordinate
from typing import Dict, List, Set


class TestBoard(unittest.TestCase):

    def setUp(self):
        my_snake = Snake({'id': '1','name': 'name1','health': 100,'body': [{'x': 2, 'y': 2}, {'x': 2, 'y': 3}],'latency': 0,'shout': '','squad': '','customizations': []})
        my_snake_oob = Snake({'id': '1','name': 'name1','health': 100,'body': [{'x': -1, 'y': 2}, {'x': 2, 'y': 3}],'latency': 0,'shout': '','squad': '','customizations': []})
        my_snake_implode = Snake({'id': '1','name': 'name1','health': 100,'body': [{'x': 2, 'y': 2}, {'x': 1, 'y': 2}, {'x': 1, 'y': 1}, {'x': 2, 'y': 1},{'x': 2, 'y': 2}],'latency': 0,'shout': '','squad': '','customizations': []})
        my_snake_crash = Snake({'id': '1','name': 'name1','health': 100,'body': [{'x': 2, 'y': 2}, {'x': 2, 'y': 1}],'latency': 0,'shout': '','squad': '','customizations': []})
        
        board_distance_json = {
            'height': 10,'width': 10,'food': [{'x': 1, 'y': 1}],'hazards': [],
            'snakes': [my_snake.get_json()]
        }
        
        board_hazard_json = {
            'height': 10,'width': 10,'food': [],'hazards': [{'x': 2, 'y': 2}],
            'snakes': [my_snake.get_json()]
        }

        board_oob_json = {
            'height': 10,'width': 10,'food': [],'hazards': [],
            'snakes': [my_snake_oob.get_json()]
        }

        board_implode_json = {
            'height': 10,'width': 10,'food': [],'hazards': [],
            'snakes': [my_snake_implode.get_json()]
        }

        board_crash_json = {
            'height': 10,'width': 10,'food': [],'hazards': [],
            'snakes': [my_snake.get_json(), my_snake_crash.get_json()],
        }

        board_food_json = {
            'height': 10,'width': 10,'food': [{'x': 2, 'y': 2}],'hazards': [],
            'snakes': [my_snake.get_json()]
        }
        

        self.board_distance = Board(board_distance_json, my_snake)
        self.board_hazard = Board(board_hazard_json, my_snake)
        self.board_oob = Board(board_oob_json, my_snake_oob)
        self.board_implode = Board(board_implode_json, my_snake_implode)
        self.board_crash = Board(board_crash_json, my_snake_crash)
        self.board_food = Board(board_food_json, my_snake)

    def test_distance_to_nearest_food(self):
        result = self.board_distance.distance_to_nearest_food()
        distance = Coordinate.euclidean_distance({'x': 1, 'y': 1}, {'x': 2, 'y': 2})
        self.assertEqual(distance, result) 

    def test_clean_corpses_hazard(self):
        cleaned_board = self.board_hazard.clean_corpses()
        self.assertEqual(len(cleaned_board.all_snakes), 0)
        self.assertEqual(cleaned_board.my_snake, None)        

    def test_clean_corpses_oob(self):
        cleaned_board = self.board_oob.clean_corpses()
        self.assertEqual(len(cleaned_board.all_snakes), 0)
        self.assertEqual(cleaned_board.my_snake, None)     

    def test_clean_corpses_implode(self):
        cleaned_board = self.board_implode.clean_corpses()
        self.assertEqual(len(cleaned_board.all_snakes), 0)
        self.assertEqual(cleaned_board.my_snake, None)        
    
    def test_clean_corpses_crash(self):
        cleaned_board = self.board_crash.clean_corpses()
        self.assertEqual(len(cleaned_board.all_snakes), 0)
        self.assertEqual(cleaned_board.my_snake, None)    

    def test_clean_food(self):
        self.assertEqual(len(self.board_food.food), 1)
        cleaned_board = self.board_food.clean_foods()
        self.assertEqual(len(cleaned_board.food), 0)

if __name__ == '__main__':
    unittest.main()