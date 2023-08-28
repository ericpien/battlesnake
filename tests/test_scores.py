import unittest
import sys
sys.path.append(r"battlesnake/components")
from board import Board
from snake import Snake
from coordinate import Coordinate
from typing import Dict, List, Set


class TestScore(unittest.TestCase):

    def setUp(self):
        my_snake = Snake({'id': '1','name': 'name1','health': 100,'body': [{'x': 2, 'y': 2}, {'x': 2, 'y': 3}],'latency': 0,'shout': '','squad': '','customizations': []})
        weak_snake = Snake({'id': '1','name': 'name1','health': 50,'body': [{'x': 3, 'y': 3}, {'x': 3, 'y': 4}],'latency': 0,'shout': '','squad': '','customizations': []})
        other_snake = Snake({'id': '2','name': 'name2','health': 100,'body': [{'x': 2, 'y': 2}, {'x': 2, 'y': 3}],'latency': 0,'shout': '','squad': '','customizations': []})
        
        
        board_max_json = {
            'height': 10,'width': 10,'food': [{'x': 2, 'y': 2}],'hazards': [],
            'snakes': [my_snake.get_json()]
        }

        board_hungry_json = {
            'height': 10,'width': 10,'food': [{'x': 9, 'y': 9}],'hazards': [],
            'snakes': [my_snake.get_json()]
        }

        board_neutral_json = {
            'height': 10,'width': 10,'food': [],'hazards': [],
            'snakes': [my_snake.get_json()]
        }

        board_weak_json = {
            'height': 10,'width': 10,'food': [],'hazards': [],
            'snakes': [weak_snake.get_json()]
        }

        board_dead_json = {
            'height': 10,'width': 10,'food': [],'hazards': [],
            'snakes': [other_snake.get_json()]
        }
        

        self.board_max = Board(board_max_json, my_snake)
        self.board_hungry = Board(board_hungry_json, my_snake)
        self.board_neutral = Board(board_neutral_json, my_snake)
        self.board_weak = Board(board_weak_json, weak_snake)
        self.board_dead = Board(board_dead_json, my_snake)

    def test_score(self):
        self.assertEquals(self.board_neutral.score_board(),self.board_neutral.score_board())
        self.assertTrue(self.board_neutral.score_board() > self.board_weak.score_board())
        self.assertTrue(self.board_hungry.score_board() < self.board_max.score_board())
        self.assertTrue(self.board_neutral.score_board() > self.board_dead.score_board())
        
    def test_permute(self):
        scores = self.board_hungry.score_moves(3)
        print(scores)

        scores = self.board_dead.score_moves(3)
        print(scores)

        scores = self.board_neutral.score_moves(3)
        print(scores)

        scores = self.board_max.score_moves(3)
        print(scores)

        # permuted_boards: deque = deque()

        for move in ["up","right","down","left"]:
            permuted_board = self.board_neutral.permute_ours(move)
            # permuted_boards.append(permuted_board)
            print(permuted_board.my_snake.get_json())
            print(permuted_board.score_board())
            # print(permuted_board.board_to_np())

        


if __name__ == '__main__':
    unittest.main()