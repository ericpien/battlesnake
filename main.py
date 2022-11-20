''' 
ericpien's notes

useful links: 
  - https://docs.battlesnake.com
  - https://docs.battlesnake.com/api/objects/battlesnake

'''

import random
import typing
import numpy as np
import math

snake_name = "Slytherin" # source: https://play.battlesnake.com/u/ericpien/#battlesnakes

# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "ericpien",  # Battlesnake Username
        "color": "#FA4616",    # Choose color
        #"head": "do-sammy",  # Choose head
        "head": "tiger-king",  # Choose head
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

    is_move_safe = {
      "up": True, 
      "down": True, 
      "left": True, 
      "right": True
    }

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
  
    for snake in snakes:
      if (snake["name"] != snake_name):
        op_body_before_tail += snake['body'][:-1]
        snake_head_x = snake["head"]["x"]
        snake_head_y = snake["head"]["y"]
        op_head_next_positions += [{'x': snake_head_x+1, 'y':snake_head_y}] #go right
        op_head_next_positions += [{'x': snake_head_x-1, 'y':snake_head_y}] #go left
        op_head_next_positions += [{'x': snake_head_x, 'y':snake_head_y+1}] #go up
        op_head_next_positions += [{'x': snake_head_x, 'y':snake_head_y-1}] #go down

    op_next_positions = op_body_before_tail + op_head_next_positions
  
    if (my_head_left in op_next_positions):
      is_move_safe["left"] = False
      print("avoid opponent")
      
    if (my_head_right in op_next_positions):
      is_move_safe["right"] = False
      print("avoid opponent")
    
    if (my_head_down in op_next_positions):
      is_move_safe["down"] = False
      print("avoid opponent")
      
    if (my_head_up in op_next_positions):
      is_move_safe["up"] = False
      print("avoid opponent")

      
    # Prevent Battlesnake from colliding with hazards
    hazards = game_state['board']['hazards'] #array of positions [({"x":, "y": }), ...]
  
    if (my_head_left in hazards):
      is_move_safe["left"] = False
      print("avoid hazard")
      
    if (my_head_right in hazards):
      is_move_safe["right"] = False
      print("avoid hazard")
    
    if (my_head_down in hazards):
      is_move_safe["down"] = False
      print("avoid hazard")
      
    if (my_head_up in hazards):
      is_move_safe["up"] = False
      print("avoid hazard")

    
    # Are there any safe moves left?
    safe_moves = []

    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # Choose a random move from the safe ones
    next_move = random.choice(safe_moves)

    # Move towards food
    food = game_state['board']['food'] #array of (x,y) [{"x":, "y": }]

    if len(food) == 0:
      next_move = next_move
    else:
      food_distances = [euclidean_distance(f,my_head) for f in food]
      nearest_food_integer = food_distances.index(min(food_distances))
      nearest_food = food[nearest_food_integer]

      distances = {"left": euclidean_distance(my_head_left, nearest_food),
                  "right":  euclidean_distance(my_head_right, nearest_food),
                  "up":  euclidean_distance(my_head_up, nearest_food),
                  "down": euclidean_distance(my_head_down, nearest_food)}
      
      safe_move_distances = [distances[m] for m in safe_moves]
      best_move_integer = safe_move_distances.index(min(safe_move_distances))
      best_move = safe_moves[best_move_integer]
      next_move = best_move
  
    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}

def euclidean_distance(coord1, coord2):
    n = math.sqrt((coord1["x"]-coord2["x"])**2 + (coord1["y"]-coord2["y"])**2)
    return n
  
# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({
        "info": info, 
        "start": start, 
        "move": move, 
        "end": end
    })
