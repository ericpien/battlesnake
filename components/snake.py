# from .coordinate import Coordinate
# import coordinate

import sys
sys.path.append(r"battlesnake/components")
from coordinate import Coordinate

from collections import deque
import copy


# Snake is any snake on the board
class Snake:

  def __init__(self, snake_json: dict):
    self.id: str = snake_json['id']
    self.name: str = snake_json['name']
    self.health: int = snake_json['health']
    self.body: deque = deque(snake_json['body'])
    self.latency: int = snake_json['latency']
    self.length: int = len(self.body)
    self.shout: str = snake_json['shout']
    self.squad: list = snake_json['squad']
    self.customizations: dict = snake_json['customizations']

  # two snakes are equal if their id are equal
  def __eq__(self, other):
    return (self.id == other.id)

  # given snake, find out the safe moves to make
  def safe_moves(self) -> deque:
    safe_moves = deque()

    head = Coordinate(self.body[0])
    neck = Coordinate(self.body[1])
    parts: set = set()
    for part in list(self.body)[1:]:
      parts.add(Coordinate(part))
    
    if head.move_left() not in parts:
      safe_moves.append("left")

    if head.move_up() not in parts:
      safe_moves.append("up")

    if head.move_right() not in parts:
      safe_moves.append("right")

    if head.move_down() not in parts:
      safe_moves.append("down")

    return safe_moves

  def alive(self, board_width, board_height, board_hazards) -> bool:
    if any([
        self.body[0]['x'] not in range(0, board_width), 
        self.body[0]['y'] not in range(0, board_height), 
        Coordinate(self.body[0]) in board_hazards
      ]):
      return False

    return True

  # given move, perform action and return snake
  def move(self, foods: set[dict], move: str) -> 'Snake':
    new_snake = copy.copy(self)
    new_body = deque(self.body)

    if move == 'up':
      new_body.appendleft(Coordinate(self.body[0]).move_up().__dict__)

    elif move == 'down':
      new_body.appendleft(Coordinate(self.body[0]).move_down().__dict__)

    elif move == 'right':
      new_body.appendleft(Coordinate(self.body[0]).move_right().__dict__)

    else: # move == 'left':
      new_body.appendleft(Coordinate(self.body[0]).move_left().__dict__)

    if Coordinate(new_body[0]) in foods:
      new_snake.length += 1
    else:
      new_body.pop()

    new_snake.body = new_body
    return new_snake

  # go through safe number of moves
  def permute(self, foods: set[dict]) -> deque['Snake']:
    new_snakes = deque()
    # safe_moves = self.safe_moves()
    safe_moves = ["left","up","right","down"]

    for move in safe_moves:
      new_snakes.append(self.move(foods, move))

    return new_snakes

  def get_json(self) -> dict:
    json = {
      'id': self.id,
      'name': self.name,
      'health': self.health,
      'body': list(self.body),
      'latency': self.latency,
      'head': self.body[0],
      'length': self.length,
      'shout': self.shout,
      'squad': self.squad,
      'customizations': self.customizations
    }
    return json