import sys
sys.path.append(r"battlesnake/components")
from snake import Snake
from coordinate import Coordinate

from collections import deque
import numpy as np
from statistics import mean
import copy
import itertools


def flatten(lolox: list[list]) -> set[dict]:
  lox = set()
  for l in lolox:
    lox.add(l)
  return lox


class Board:
  def __init__(self, board_json: dict, my_snake: 'Snake'):
    self.height: int = board_json['height']
    self.width: int = board_json['width']
    self.food: set = set() 
    self.hazards: set = set()
    self.my_snake: "Snake" = my_snake  # if (my_snake.id in [s['id'] for s in board_json['snakes']]) else False  # Snake or empty
    self.other_snakes: deque["Snake"] = deque()
    self.all_snakes: deque["Snake"] = deque()
    

    for food in board_json['food']:
      self.food.add(Coordinate(food))

    for hazard in board_json['hazards']:
      self.hazards.add(Coordinate(hazard))

    for snake in board_json['snakes']:
      self.all_snakes.append(Snake(snake))

      if Snake(snake) != my_snake:
        self.other_snakes.append(Snake(snake))
  
  def distance_to_nearest_food(self) -> int:
    if len(self.food) == 0:
      return 0
    
    return min(Coordinate.euclidean_distance(f, self.my_snake.body[0]) for f in  self.food)
      
    
  def clean_corpses(self) -> "Board":
    new_board = copy.copy(self)

    snake_part_count: dict[dict("x","y"), int] = {}
    snakes_to_kill: deque = deque()

    for snake in self.all_snakes:
        for part in snake.body:
          part_coord = Coordinate(part)
          if (snake_part_count.get(part_coord) == None):
              snake_part_count[part_coord] = 1
          else:
              snake_part_count[part_coord] += 1
    
    for snake in self.all_snakes:
      if snake_part_count.get(Coordinate(snake.body[0])) > 1:
        snakes_to_kill.append(snake)
      elif not snake.alive(self.width, self.height, self.hazards):
        snakes_to_kill.append(snake)

    for snake in snakes_to_kill:
      if snake == self.my_snake:
        new_board.my_snake = None
      else:
        new_board.other_snakes.remove(snake)
      
      new_board.all_snakes.remove(snake)

    return new_board
  
  def clean_foods(self) -> "Board":
    new_board = copy.copy(self)
    snake_heads = set()
    
    for snake in self.all_snakes:
      snake_heads.add(Coordinate(snake.body[0]))

    filtered_food = set()

    for food in self.food:
      if food not in snake_heads:
        filtered_food.add(food)

    new_board.food = filtered_food
    return new_board

  def all_snakes_json(self) -> list[dict]:

    return [s.get_json() for s in self.all_snakes]

  def score_board(self) -> int:
    
    death_aversion = 0
    food_seeking = 0
    length = 0
    bravery = 0
    aggression = 0
    health = 0

    if not self.my_snake:
      death_aversion = -5_000
      return death_aversion

    else:
      aggression = len(self.other_snakes) * -10
      length = (self.my_snake.length - 3) * 1_000
      health = self.my_snake.health 
      if len(self.food) > 0:
         food_seeking = self.distance_to_nearest_food() * -100

      factors = [death_aversion, food_seeking, aggression, bravery, length, health]
      return int(mean(factors))


  def score_moves(self, n: int) -> dict:
    moves = ["up","down","left","right"]
    scored_moves = {}
    for move in moves:
      scored_moves[move] = self.score_n_steps(moves=[move], n=n, counter=0)

    return scored_moves

  def score_n_steps(self, moves: list, n: int, counter: int = 0) -> float:
    '''
    : n: n depth to traverse
    : counter: current depth. Initialized at 0
    : scores: List of scores. Initialized at []
    '''

    # If traversed far enough, return score
    if counter >= n:
      return self.score_board()

    # If I'm dead, no point traverseing further.
    elif not self.my_snake:
      return self.score_board()

    # If none of the above is true, continue the journey
    counter += 1
    scores = deque()
    our_move_boards = deque()
    their_move_boards = deque()
    cleaned_boards = deque()

    # for each move passed, permute my_snake
    for move in moves:
      # Create all boards based on our move + their moves
      our_move_boards.append(self.permute_ours(move))

    if (len(self.other_snakes) != 0):
      # for each of my permutation, permute other_snakes
      for board in our_move_boards:
        their_move_boards += board.permute_theirs()
    else:
      their_move_boards = our_move_boards

    for board in their_move_boards:
      cleaned_board = board.clean_corpses()
      scores.append(cleaned_board.score_board())
      cleaned_boards.append(cleaned_board.clean_foods())


    # for each node, permute and add
    for board in cleaned_boards:
      scores.append(board.score_n_steps(["up","down","left","right"], n, counter))

    #print('depth: {} | moves: {} | scores: {}'.format(counter,moves,scores))
    return int(mean(scores) * 0.75)
  
  
  def permute_ours(self, move: str) -> 'Board':
    new_board = copy.copy(self)

    new_board.my_snake = new_board.my_snake.move(foods = self.food,move = move)

    return new_board

  def permute_theirs(self) -> deque['Board']:
    permuted_boards: deque["Board"] = deque()

    #1 given other snakes, make all combination of them into list of Boards
    new_snakes: deque = deque()  #Listof Listof Snakes
    new_boards: deque = deque() #Listof Listof Boards

    for snake in self.other_snakes:
    #create all moves for each other_snakes
      new_snakes.append(snake.permute(foods = self.food))

    combinations = [list(tup) for tup in (itertools.product(*new_snakes))]

    for los in combinations:
      # apply new snake combination to board's others
      new_board = copy.copy(self)
      new_board.other_snakes = deque(los)
      new_board.all_snakes = deque([new_board.my_snake]) + new_board.other_snakes

      new_boards.append(new_board)

    return new_boards






  def board_to_np(self) -> np.ndarray:
    # Use the enum values to populate a 2d array
    '''
      : Convert coord (x,y) to nd index for visual purpose with [10-y] [x]
      Representation:
      _: Empty
      F: Food
      H: Hazard
      0: my_snake
      n: other_snakes, n: int > 0
      nA: snake's head
      example:
      10 [['__', '__', '__', '__', '__', '__', '__', '__', '__', '__', '__'],
       9 ['__', '__', '__', '__', '__', '__', '__', '__', '__', '__', '__'],
       8 ['__', '__', '__', '__', '__', '__', '__', '__', '__', '__', '__'],
       7 ['__', '__', '__', '__', '__', '__', '__', '__', '__', '__', '__'],
       6 ['__', '__', '__', '__', '__', '__', '__', '__', '__', '__', '__'],
       5 ['__', '__', '__', '__', '__', '__', '__', '__', '__', '__', '__'],
       4 ['__', '__', '__', '__', '__', '__', '__', '__', '__', '__', '__'],
       3 ['__', '__', '__', '__', '__', '__', '__', '__', '__', '__', '__'],
       2 ['__', '_1', '_H', '__', '__', '__', '__', '__', '__', '__', '__'],
       1 ['__', '_1', 'A0', '_0', '_0', '__', '__', '__', '__', '__', '__'],
       0 ['__', '1A', '_F', '__', '__', '__', '__', '__', '__', '__', '__']]
            0     1     2     3     4     5     6     7     8     9    10
      '''

    # Initiate the full board as empty given the width/height
    table = np.full((self.height, self.width), "__")

    #
    for f in self.food:
      table[self.height - f['y'] - 1][f['x']] = "_F"

    for h in self.hazards:
      table[self.height - h['y'] - 1][h['x']] = "_H"

    if self.my_snake:
      table[self.height - self.my_snake.body[0]['y'] -
            1][self.my_snake.body[0]['x']] = "A0"
      for b in self.my_snake.body[1:]:
        table[self.height - b['y'] - 1][b['x']] = "_0"

    for c, s in enumerate(self.other_snakes):
      table[self.height - s.body[0]['y'] - 1][s.body[0]['x']] = "A" + str(c + 1)
      for b in s.body[1:]:
        table[self.height - b['y'] - 1][b['x']] = "_" + str(c + 1)

    return table

  
