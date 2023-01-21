''' 
ericpien's notes

useful links: 
  - https://docs.battlesnake.com
  - https://docs.battlesnake.com/api/objects/battlesnake

'''

import pandas as pd
import numpy as np
from statistics import mean
from statistics import median
from statistics import mode
import typing
from typing import List
from typing import Dict
import copy
import math
import random
import itertools


# Represent X and Y coordinates and perform operations on them
class Coordinate:

  # Coordinate has these constants for quick operations
  LEFT  = {'x': -1, 'y':  0}
  RIGHT = {'x':  1, 'y':  0}
  UP    = {'x':  0, 'y':  1}
  DOWN  = {'x':  0, 'y': -1}

  def __init__(self, xy: Dict):
    # Initialize coordinate using a dictionary {'x': int, 'y': int}
    self.x = xy['x']
    self.y = xy['y']

  def __add__(self, coord2: "Coordinate") -> "Coordinate":
    # Add current coordinate to coord2 and return new coordinate
    return Coordinate(self.x + coord2.x, self.y + coord2.y)
  
  def __str__(self):
    # Print Coordinate (x,y)
    return "('x': {}, 'y' {})".format(self.x,self.y)
  
  def move_left(self) -> "Coordinate":
    # Move coordinate point one LEFT
    return Coordinate({'x': self.x + self.LEFT['x'], 'y':self.y + self.LEFT['y']})
  
  def move_right(self) -> "Coordinate":
    # Move coordinate point one RIGHT
    return Coordinate({'x': self.x + self.RIGHT['x'], 'y':self.y + self.RIGHT['y']})

  def move_up(self) -> "Coordinate":
    # Move coordinate point one UP
    return Coordinate({'x': self.x + self.UP['x'], 'y':self.y + self.UP['y']})

  def move_down(self) -> "Coordinate":
    # Move coordinate point one DOWN
    return Coordinate({'x': self.x + self.DOWN['x'], 'y':self.y + self.DOWN['y']})

  def euclidean_distance(coord1:Dict, coord2: Dict) -> float:
    # Return the euclidean distance from current coordinate to coord2
    n = math.sqrt((coord1['x']-coord2['x'])**2 + (coord1['y']-coord2['y'])**2)
    return n
    
  
# Snake is any snake on the board
class Snake:
    def __init__(self,snake_json: Dict):       
        self.id = snake_json['id']
        self.name = snake_json['name']
        self.health = snake_json['health']
        self.body = snake_json['body']
        self.latency = snake_json['latency']
        self.head = snake_json['head']
        self.length = snake_json['length']
        self.shout = snake_json['shout']
        self.squad = snake_json['squad']
        self.customizations = snake_json['customizations']

    def move(self, foods: List[Dict], move: str) -> 'Snake':
        x = copy.deepcopy(self)
        new_body = []
        
        if move == 'up':
            new_body = [Coordinate(self.head).move_up().__dict__] + self.body
        elif move == 'down':
            new_body = [Coordinate(self.head).move_down().__dict__] + self.body
        elif move == 'right':
            new_body = [Coordinate(self.head).move_right().__dict__] + self.body
        elif move == 'left':
            new_body = [Coordinate(self.head).move_left().__dict__] + self.body

        if new_body[0] in foods:
            x.body = new_body
            x.head = new_body[0]
        else:
            x.body = new_body[:-1]
            x.head = new_body[0]

        return x

    def get_snake(self) -> Dict:
        json =  {
            'id':self.id,
            'name':self.name,
            'health':self.health,
            'body':self.body,
            'latency': self.latency,
            'head': self.head,
            'length': self.length,
            'shout': self.shout,
            'squad': self.squad,
            'customizations': self.customizations
            }
        return json

class Board:
  DEAD = -10_000
  MOVES = ['up','down','left','right']

  def __init__(self,board_json: Dict, my_snake: 'Snake'):
    self.height       = board_json['height']
    self.width        = board_json['width']
    self.food         = board_json['food']
    self.hazards      = board_json['hazards']
    self.my_snake     = my_snake if (my_snake.id in [s['id'] for s in board_json['snakes']]) else []  # Snake or empty
    self.other_snakes = [Snake(s) for s in board_json['snakes'] if s['id'] != my_snake.id]            # list of Snake
  
  def permute_ours(self, safe_moves: List) -> List['Board']:
    new_boards = []
    
    for move in safe_moves:
      new_board = copy.deepcopy(self)
      my_snake_moved = self.my_snake.move(foods = self.food, move = move)
      new_board.my_snake = my_snake_moved
      new_board.food = [f for f in new_board.food if f != my_snake_moved.head]
      new_boards += [new_board]
    
    return new_boards

  def permute_theirs(self) -> List['Board']:
    
    #1 if no other snakes, return self
    if len(self.other_snakes) <= 0:
      return self

    #2 # given other snakes, make all combination of them into list of Boards
    new_snakes   = [] #Listof Listof Snakes
    new_boards   = [] #Listof Listof Boards

    for snake in self.other_snakes:
      #create all moves for each other_snakes
      new_snakes += [[snake.move(foods = self.food, move = move) for move in self.MOVES]]

    combinations = [list(tup) for tup in (itertools.product(*new_snakes))]
    
    for los in combinations:
      # apply new snake combination to board's others
      new_board = copy.deepcopy(self)
      new_board.other_snakes = los
      new_boards += [new_board.clean_board()]

    return new_boards

  
  def clean_board(self) -> "Board":
    
    #1 remove my snake if it's not meant to be
    new_board = copy.deepcopy(self)

    if not self.my_snake_status():
      new_board.my_snake = []

    #2 remove food if eaten
    snake_heads = [sn.head for sn in self.other_snakes + [self.my_snake]]
    filtered_food = [f for f in self.food if f not in snake_heads]
    new_board.food = filtered_food

    #3 filter snakes if its head is out of bounds / in hazard / in itself
    snakes_to_remove = [] #list of index to pop

    for c, sn in enumerate(self.other_snakes):
      if any([sn.head in self.hazards, 
              sn.head['x'] not in range(0,self.width),
              sn.head['y'] not in range(0,self.height),
              sn.head in sn.body[1:]]):
        snakes_to_remove += [c]
      else:
        others = self.other_snakes[:c] + self.other_snakes[c+1:] + [self.my_snake]
        if sn.head in flatten([s.body for s in others]):
          snakes_to_remove += [c]

    if len(snakes_to_remove) > 0:
      snakes_to_remove.reverse()

      for i in snakes_to_remove:
        new_board.other_snakes.pop(i)

    return new_board
  
  def score(self) -> float:
      death_aversion = 0
      hunger_aversion = 0
      aggression = 0      
    
      if self.my_snake == []:
          death_aversion = self.DEAD
          factors = [death_aversion, hunger_aversion, aggression]
          return int(death_aversion)
      
      else:
          #hunger_aversion = (self.my_snake.health - 100)*100    
          #aggression = len(self.other_snakes)*-10
          factors = [death_aversion, hunger_aversion, aggression]
          return int(mean(factors))
  
  def all_snakes_json(self) -> List[Dict]:
    
    return [s.get_snake() for s in [self.my_snake]] + [s.get_snake() for s in self.other_snakes]

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
    elif self.my_snake == []:
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
        if not board.my_snake_status():
            scores += [self.DEAD]
            our_move_boards.remove(board)

        elif len(board.other_snakes) != 0:
            their_move_boards += board.permute_theirs()

    # finalize the board based on other_snake status
    permuted_boards = our_move_boards if len(their_move_boards) == 0 else their_move_boards

    # for each node, permute and add
    for board in permuted_boards:
        scores += [board.score_n_steps(self.MOVES,n,counter)]
        
    
    #print('depth: {} | moves: {} | scores: {}'.format(counter,moves,scores))

    return int(mean(scores))    

  def my_snake_status(self) -> bool:
    if any([self.my_snake.head in self.my_snake.body[1:],
        self.my_snake.head['x'] not in range(0,self.width),
        self.my_snake.head['y'] not in range(0,self.height),
        self.my_snake.head in flatten([s.get_snake()['body'] for s in self.other_snakes]),
        self.my_snake.head in self.hazards]):
        return False
    else:
        return True

  def score_moves(self, moves: List, n: float) -> Dict:
    scored_moves = {}
    for move in moves:
        scored_moves[move] = self.score_n_steps(moves = [move], n = n, counter = 0)

    return scored_moves
  
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
      table = np.full((self.height,self.width),"__")
    
      # 
      for f in self.food:
        table[self.height-f['y']-1][f['x']] = "_F"
      
      for h in self.hazards:
        table[self.height-h['y']-1][h['x']] = "_H"
      
      if self.my_snake != []:
        table[self.height-self.my_snake.head['y']-1][self.my_snake.head['x']] = "A0"
        for b in self.my_snake.body[1:]:
            table[self.height-b['y']-1][b['x']] = "_0"
        
      for c, s in enumerate(self.other_snakes):
        table[self.height-s.head['y']-1][s.head['x']] = "A"+str(c+1)
        for b in s.body[1:]:
            table[self.height-b['y']-1][b['x']] = "_"+str(c+1)

      return table



class BoardTile():
  pass

class BoardTree:
  def __init__(init_state: Board):
  # Build the tree from our initial state by permuting
    pass




def flatten(lolox: List[List]) -> List:
    lox = []
    for l in lolox:
        lox += l
    return lox

# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "ericpien",  # Battlesnake Username
        "color": "#FA4616",    # Choose color
        "head": "do-sammy",  # Choose head
       # "head": "tiger-king",  # Choose head
        "tail": "nr-booster",  # Choose tail
    }

# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")

# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")

# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:
    print('\nTURN {}'.format(game_state['turn']))
  
    is_move_safe = {
      "up": True, 
      "down": True, 
      "left": True, 
      "right": True
    }

    my_snake = Snake(game_state["you"])
    bd = Board(game_state['board'],my_snake)
    
    safe_moves = ['up','down','left','right']
    score_dict = bd.score_moves(safe_moves, 2)

    summary = pd.DataFrame(list(score_dict.items()),columns=['moves','scores'])
  
    if len(summary) == 0:
      print("No safe moves detected! Going rogue!!")
      next_move = random.choice(safe_moves)
      return {"move": next_move}

    
    max_score = max(summary['scores'])
    best_next_moves = []
    for i in range(len(summary)):
      if summary['scores'][i] == max_score:
          best_next_moves.append(summary['moves'][i])
    
  
    safe_moves = best_next_moves
    print(summary)
    print('available moves are: {}'.format(safe_moves))  
  
  # Move towards food
    food = game_state['board']['food'] #array of (x,y) [{"x":, "y": }]

    if len(food) == 0:
      next_move = random.choice(safe_moves)
    else:
      food_distances = [Coordinate.euclidean_distance(f,my_snake.head) for f in food]
      nearest_food_integer = food_distances.index(min(food_distances))
      nearest_food = food[nearest_food_integer]

      

      distances = {"left": Coordinate.euclidean_distance(Coordinate(my_snake.head).move_left().__dict__,  nearest_food),
                  "right": Coordinate.euclidean_distance(Coordinate(my_snake.head).move_right().__dict__, nearest_food),
                  "up"   : Coordinate.euclidean_distance(Coordinate(my_snake.head).move_up().__dict__,    nearest_food),
                  "down" : Coordinate.euclidean_distance(Coordinate(my_snake.head).move_down().__dict__,  nearest_food)}
      
      safe_move_distances = [distances[m] for m in safe_moves]
      best_move_integer = safe_move_distances.index(min(safe_move_distances))
      best_move = safe_moves[best_move_integer]
      next_move = best_move
  
    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}

if __name__ == "__main__":
    from server import run_server

    run_server({
        "info": info, 
        "start": start, 
        "move": move, 
        "end": end
    })