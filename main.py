''' 
ericpien's notes

useful links: 
  - https://docs.battlesnake.com
  - https://docs.battlesnake.com/api/objects/battlesnake

'''

import pandas as pd
import numpy as np
from statistics import mean
import typing
from typing import List
from typing import Dict
import copy
import math
import random


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

    def basic_safe_moves(self, moves: Dict) -> Dict:
      # remove implosion
      
      # check out of bounds
      
      pass

class Board:
  def __init__(self,board_json: Dict):
    self.height = board_json['height']
    self.width = board_json['width']
    self.food = board_json['food']
    self.hazards = board_json['hazards']
    self.snakes = board_json['snakes']
  
  def permute_ours(self, my_snake: Snake, safe_moves: List) -> List['Board']:
    new_boards = []
    my_index = next((index for (index, d) in enumerate(self.snakes) if d["id"] == my_snake.id), None)

    for m in safe_moves:
        nboard = copy.deepcopy(self)
        new_snake = my_snake.move(foods = self.food, move = m)
        nboard.snakes[my_index] = new_snake.get_snake()
        nboard.food = [f for f in nboard.food if f != new_snake.head]
        new_boards += [nboard]

    return new_boards

  def permute_theirs(self, my_snake: Snake) -> List['Board']:
    new_snakes = [[Snake(s) for s in self.snakes if s['id'] == my_snake.id]]
    new_boards = []

    # Create new snakes
    for sn in self.snakes:
        if sn['id'] == my_snake.id:
            pass
        else: 
            new_snakes_tmp = []
            for m in ['up','down','left','right']:
                new_snake = [Snake(sn).move(foods = self.food, move = m)]
                msnakes = [s+new_snake for s in new_snakes]
                new_snakes_tmp += msnakes
            new_snakes = new_snakes_tmp
    
    # create new boards using the new snakes
    for los in new_snakes:
        new_boards += [self.filter_snakes_to_board(los)]

    return new_boards
  
  def flatten(lolox: List[List]) -> List:
    lox = []
    for l in lolox:
        lox += l
    return lox

  def filter_snakes_to_board(self, snakes: List["Snake"]) -> List["Board"]:
    
    # filter snakes if its head is out of bounds / in hazard / in itself
    # self.height / self.width / self.hazards / s.body[1:]
    filtered_snakes = [sn for sn in snakes if ((sn.head not in self.hazards) and 
                                                (sn.head['x'] >= 0) and
                                                (sn.head['x'] <= (self.width - 1)) and
                                                (sn.head['y'] >= 0) and
                                                (sn.head['y'] <= (self.height - 1)) and
                                                (sn.head not in sn.body[1:]))]

    # remove food if eaten
    # self.food
    snake_heads = [sn.head for sn in snakes]
    filtered_food = [f for f in self.food if f not in snake_heads]
   
    # remove snakes that have collided with others
    non_collided_snakes = [sn.get_snake() for sn in filtered_snakes if sn.head not in Board.flatten([s.body for s in filtered_snakes if s != sn])]
    
    # create new board with the snakes and foods
    nboard = copy.deepcopy(self)
    nboard.food = filtered_food

    nboard.snakes = non_collided_snakes
    return nboard
  
  
  def score(self, my_snake: Snake) -> float:
    death_aversion = 0
    hunger_aversion = 0
    aggression = 0      
    
    local_ids = [s['id'] for s in self.snakes]
    other_snakes = [s for s in self.snakes if s['id'] != my_snake.id]

    if my_snake.get_snake()['id'] not in local_ids:
        death_aversion = -10000
        factors = [death_aversion, hunger_aversion, aggression]
        return mean(factors)
    
    else:
        local_my_snake = [s for s in self.snakes if s['id'] == my_snake.id][0]
        hunger_aversion = (local_my_snake['health'] - 100)*100    
        aggression = len(other_snakes)*-100
        factors = [death_aversion, hunger_aversion, aggression]
        return mean(factors)
  
  def score_n_steps(self, my_snake: Snake, moves: List, counter: float, n: float) -> float:
    counter += 1
    #initiate dictionary
    print('depth: {}_____'.format(counter))
    scores = []

    for move in moves:
        try:
            local_my_snake = [Snake(s) for s in self.snakes if s['id'] == my_snake.id][0]
            # Create all boards based on our move + their moves
            our_move_boards = self.permute_ours(local_my_snake,[move])
            #print('move: {} | # our moves: {}'.format(move,len(our_move_boards)))
            all_possible_next_boards = []
            for b in our_move_boards:
                all_possible_next_boards += b.permute_theirs(local_my_snake)

            # Creating unique list out of boards
            unique_boards = [] 
            unique_snakes = []

            for b in all_possible_next_boards:
                if b.snakes not in unique_snakes:
                    unique_boards += [b]
                    unique_snakes += [b.snakes]

            #print('move: {} | # their moves: {}'.format(move,len(unique_boards)))
            
            ## Score test
            for b in unique_boards:
                local_score = b.score(local_my_snake)
                scores += [local_score]
                #print('scores: {}'.format(scores))
                print('depth: {} | move: {} | scores: {}'.format(counter,move,scores))

                if counter < n:
                    scores += [b.score_n_steps(local_my_snake,['up','down','right','left'],counter,n)]
                    
                print('depth: {} | move: {} | scores: {}'.format(counter,move,scores))

        except:
            return -10000
    
    return mean(scores)
  
  def score_moves(self, my_snake: Snake, moves: List, counter: float, n: float) -> Dict:
    scored_moves = {}
    for move in moves:
        scored_moves[move] = self.score_n_steps(my_snake, [move], counter, n)

    return scored_moves
  
  def build_np(self) -> np.ndarray:
    # Use the enum values to populate a 2d array
    pass

class BoardTile():
  pass

class BoardTree:
  def __init__(init_state: Board):
  # Build the tree from our initial state by permuting
    pass



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

    sn = Snake(game_state["you"])
    bd = Board(game_state['board'])
    
    #is_move_safe = bd.basic_safe_moves()
  
  
    # Prevent Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

    my_head_left = {"x": my_head["x"]-1, "y": my_head["y"]}
    my_head_right = {"x": my_head["x"]+1, "y": my_head["y"]}
    my_head_down = {"x": my_head["x"], "y": my_head["y"]-1}
    my_head_up = {"x": my_head["x"], "y": my_head["y"]+1}

    if my_neck["x"] < my_head["x"]:
        is_move_safe["left"] = False

    elif my_neck["x"] > my_head["x"]:
        is_move_safe["right"] = False

    elif my_neck["y"] < my_head["y"]:
        is_move_safe["down"] = False

    elif my_neck["y"] > my_head["y"]:
        is_move_safe["up"] = False

    # Prevent Battlesnake from moving out of bounds
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']

    if (my_head["x"] == 0):
        is_move_safe["left"] = False
    
    if (my_head["x"] == (board_width - 1)):
        is_move_safe["right"] = False

    if (my_head["y"] == 0):
        is_move_safe["down"] = False
    
    if (my_head["y"] == (board_height - 1)):
        is_move_safe["up"] = False

    # Prevent Battlesnake from colliding with itself
    my_body = game_state['you']['body'] #array of coords [{"x":0,"y":0},{...}]
    my_body_before_tail = my_body[:-1]
    
    if (my_head_left in my_body_before_tail):
      is_move_safe["left"] = False
    
    if (my_head_right in my_body_before_tail):
      is_move_safe["right"] = False

    if (my_head_down in my_body_before_tail):
      is_move_safe["down"] = False
   
    if (my_head_up in my_body_before_tail):
      is_move_safe["up"] = False
    
    # Prevent Battlesnake from colliding with other Battlesnakes
    snakes = game_state['board']['snakes'] #array of snakeobjects [sn, sn, sn, ...]

    op_body_before_tail = []
    op_head_next_positions = []
      
    # Prevent Battlesnake from colliding with hazards
    hazards = game_state['board']['hazards'] #array of positions [({"x":, "y": }), ...]
  
    if (my_head_left in hazards):
      is_move_safe["left"] = False
      
    if (my_head_right in hazards):
      is_move_safe["right"] = False
    
    if (my_head_down in hazards):
      is_move_safe["down"] = False
      
    if (my_head_up in hazards):
      is_move_safe["up"] = False

    

    # Are there any safe moves left?
    safe_moves = []

    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
      safe_moves = ['up','down','left','right']
      
    
    #sn = Snake(game_state["you"])
    #bd = Board(game_state['board'])
    score_dict = bd.score_moves(sn, safe_moves, 0, 2)

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
      food_distances = [Coordinate.euclidean_distance(f,my_head) for f in food]
      nearest_food_integer = food_distances.index(min(food_distances))
      nearest_food = food[nearest_food_integer]

      distances = {"left": Coordinate.euclidean_distance(my_head_left,  nearest_food),
                  "right": Coordinate.euclidean_distance(my_head_right, nearest_food),
                  "up"   : Coordinate.euclidean_distance(my_head_up,    nearest_food),
                  "down" : Coordinate.euclidean_distance(my_head_down,  nearest_food)}
      
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