import sys
sys.path.append(r"battlesnake/components")
from snake import Snake
from coordinate import Coordinate
from board import Board

from collections import deque
import numpy as np
from statistics import mean
from typing import List, Dict
import copy
import itertools



class Board_Tree:
    def __init__(self, source_board: "Board", target_n: int, current_depth: int):
        self.source_board = source_board
        self.target_n = target_n
        self.current_depth = current_depth

    

    def blossom(self) -> int:
        if self.current_depth > self.target_n:
            return 0
    
        permuted_ours: deque["Board"] = self.permute_ours()
        permuted_theirs: deque["Board"] = deque()

        for board in permuted_ours:
            permuted_theirs.append(self.permute_theirs(board))


        sum_boards = 0
        cleaned_boards: deque = deque()
        for board in permuted_theirs:
            cleaned_board = board.clean_board()
            cleaned_boards.append(cleaned_board)
            sum_boards += cleaned_board.score_board()

        sum_boards = sum_boards / len(permuted_theirs)

        if self.current_depth + 1 < self.target_n:
            for board in cleaned_boards:
                bt = Board_Tree(board, self.target_n, self.current_depth + 1)
                sum_boards += bt.blossom()
        
        return sum_boards / len()

   

    
    

    def score_n_steps(self, moves: List, n: int, counter: int = 0) -> float:
        '''
        : n: n depth to traverse
        : counter: current depth. Initialized at 0
        : scores: List of scores. Initialized at []
        '''

        # If traversed far enough, return score
        if counter >= n:
        return self.score()

        # If I'm dead, no point traverseing further.
        elif not self.my_snake:
        return self.score()

        # If none of the above is true, continue the journey
        counter += 1
        scores = []
        our_move_boards = []
        their_move_boards = []

        # for each move passed, permute my_snake
        for move in moves:
        # Create all boards based on our move + their moves
        our_move_boards += self.permute_ours([move])

        # for each of my permutation, permute other_snakes
        for board in our_move_boards:
        their_move_boards += board.permute_theirs()

        # finalize the board based on other_snake status
        permuted_boards = our_move_boards if len(
        their_move_boards) == 0 else their_move_boards

        # for each node, permute and add
        for board in permuted_boards:
        scores += [board.score_n_steps(self.MOVES, n, counter)]

        #print('depth: {} | moves: {} | scores: {}'.format(counter,moves,scores))
        return int(mean(scores) * 0.8)