''' 
ericpien's notes

useful links: 
  - https://docs.battlesnake.com
  - https://docs.battlesnake.com/api/objects/battlesnake

'''

import pandas as pd
import typing
import random

from components.board import Board
from components.coordinate import Coordinate
from components.snake import Snake


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
def info() -> typing.Dict:
  print("INFO")

  return {
    "apiversion": "1",
    "author": "ericpien",  # Battlesnake Username
    "color": "#FA4616",  # Choose color
    # "head": "do-sammy",   # Choose head
    "head": "missile",  # Choose head
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

  my_snake = Snake(game_state["you"])
  bd = Board(game_state['board'], my_snake)

  safe_moves = ['up', 'down', 'left', 'right']
  score_dict = bd.score_moves(2)

  summary = pd.DataFrame(list(score_dict.items()), columns=['moves', 'scores'])

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

  #print(score_dict)
  ##print(summary)
  #print('available moves are: {}'.format(safe_moves))

  # Move towards food
  food = game_state['board']['food']  #array of (x,y) [{"x":, "y": }]

  if len(food) == 0:
    next_move = random.choice(safe_moves)
  else:
    food_distances = [
      Coordinate.euclidean_distance(f, my_snake.body[0]) for f in food
    ]
    nearest_food_integer = food_distances.index(min(food_distances))
    nearest_food = food[nearest_food_integer]

    distances = {
      "left":
      Coordinate.euclidean_distance(
        Coordinate(my_snake.body[0]).move_left().__dict__, nearest_food),
      "right":
      Coordinate.euclidean_distance(
        Coordinate(my_snake.body[0]).move_right().__dict__, nearest_food),
      "up":
      Coordinate.euclidean_distance(
        Coordinate(my_snake.body[0]).move_up().__dict__, nearest_food),
      "down":
      Coordinate.euclidean_distance(
        Coordinate(my_snake.body[0]).move_down().__dict__, nearest_food)
    }

    safe_move_distances = [distances[m] for m in safe_moves]
    best_move_integer = safe_move_distances.index(min(safe_move_distances))
    best_move = safe_moves[best_move_integer]
    next_move = best_move

  #print(f"MOVE {game_state['turn']}: {next_move}")
  return {"move": next_move}


if __name__ == "__main__":
  from server import run_server

  run_server({"info": info, "start": start, "move": move, "end": end})
