# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data

snake_name = "test-20221113" # source: https://play.battlesnake.com/u/ericpien/#battlesnakes

def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "ericpien",  # Battlesnake Username
        "color": "#FA4616",    # Choose color
        "head": "do-sammy",  # Choose head
        #"head": "tiger-king",  # Choose head
        "tail": "tiger-tail",  # Choose tail
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

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False

    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False

    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False

    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False

      
    # Prevent Battlesnake from moving out of bounds
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']

    if (my_head["x"] == 0):
        is_move_safe["left"] = False
        print('wall at ' + str(my_head["x"]))
    
    if (my_head["x"] == (board_width - 1)):
        is_move_safe["right"] = False
        print('wall at ' + str(my_head["x"]))

    if (my_head["y"] == 0):
        is_move_safe["down"] = False
        print('wall at ' + str(my_head["y"]))
    
    if (my_head["y"] == (board_height - 1)):
        is_move_safe["up"] = False
        print('wall at ' + str(my_head["y"]))

      
    # Prevent Battlesnake from colliding with itself
    my_body = game_state['you']['body'] #array of coords [{"x":0,"y":0},{...}]
    my_body_before_tail = my_body[:-1]
    # if head[x] - 1 is in body, don't turn left
    head_temp = my_head.copy()
    head_temp["x"] -= 1
    if (head_temp in my_body_before_tail):
      is_move_safe["left"] = False
    # if head[x] + 1 is in body, don't turn right
    head_temp = my_head.copy()
    head_temp["x"] += 1
    if (head_temp in my_body_before_tail):
      is_move_safe["right"] = False
    # if head[y] - 1 is in body, don't turn down
    head_temp = my_head.copy()
    head_temp["y"] -= 1
    if (head_temp in my_body_before_tail):
      is_move_safe["down"] = False
    # if head[y] + 1 is in body, don't turn up
    head_temp = my_head.copy()
    head_temp["y"] += 1
    if (head_temp in my_body_before_tail):
      is_move_safe["up"] = False

      
    # Prevent Battlesnake from colliding with other Battlesnakes
    snakes = game_state['board']['snakes']
    # array of battlesnake objects
    # https://docs.battlesnake.com/api/objects/battlesnake

    op_body_before_tail = []
    op_head_next_positions = []
    if (len(snakes) > 1):
      print('snakes detected')
      
    for snake in snakes:
      if (snake["name"] != snake_name):
        op_body_before_tail += snake['body'][:-1]
        snake_head_x = snake["head"]["x"]
        snake_head_y = snake["head"]["y"]
        op_head_next_positions += [{'x': snake_head_x+1, 'y':snake_head_y}] #go right
        op_head_next_positions += [{'x': snake_head_x-1, 'y':snake_head_y}] #go left
        op_head_next_positions += [{'x': snake_head_x, 'y':snake_head_y+1}] #go up
        op_head_next_positions += [{'x': snake_head_x, 'y':snake_head_y-1}] #go down

    my_head_left = {"x": my_head["x"]-1, "y": my_head["y"]}
    my_head_right = {"x": my_head["x"]+1, "y": my_head["y"]}
    my_head_down = {"x": my_head["x"], "y": my_head["y"]-1}
    my_head_up = {"x": my_head["x"], "y": my_head["y"]+1}

    op_next_positions = op_body_before_tail + op_head_next_positions
  
    if (my_head_left in op_next_positions):
      is_move_safe["left"] = False
      print("avoid opponent")
      
    elif (my_head_right in op_next_positions):
      is_move_safe["right"] = False
      print("avoid opponent")
    
    elif (my_head_down in op_next_positions):
      is_move_safe["down"] = False
      print("avoid opponent")
    elif (my_head_up in op_next_positions):
      is_move_safe["up"] = False
      print("avoid opponent")
      
    """
    # if head[x] - 1 is in body, don't turn left
    head_temp = my_head.copy()
    head_temp["x"] -= 1
    if (head_temp in op_body_before_tail):
      is_move_safe["left"] = False
      print('op')
    # if head[x] + 1 is in body, don't turn right
    head_temp = my_head.copy()
    head_temp["x"] += 1
    if (head_temp in op_body_before_tail):
      is_move_safe["right"] = False
      print('op')
    # if head[y] - 1 is in body, don't turn down
    head_temp = my_head.copy()
    head_temp["y"] -= 1
    if (head_temp in op_body_before_tail):
      is_move_safe["down"] = False
      print('op')
    # if head[y] + 1 is in body, don't turn up
    head_temp = my_head.copy()
    head_temp["y"] += 1
    if (head_temp in op_body_before_tail):
      is_move_safe["up"] = False
      print('op')
    
    # if head[x] + 1 is in op's next moves, don't turn right
    head_temp = my_head.copy()
    head_temp["x"] -= 1
    if (head_temp in op_head):
      is_move_safe["left"] = False
      print('op head')
    # if head[x] + 1 is in op's next moves, don't turn right
    head_temp = my_head.copy()
    head_temp["x"] += 1
    if (head_temp in op_head):
      is_move_safe["right"] = False
      print('op head')
    # if head[y] - 1 is in op's next moves, don't turn down
    head_temp = my_head.copy()
    head_temp["y"] -= 1
    if (head_temp in op_head):
      is_move_safe["down"] = False
      print('op head')
    # if head[y] + 1 is in op's next moves, don't turn up
    head_temp = my_head.copy()
    head_temp["y"] += 1
    if (head_temp in op_head):
      is_move_safe["up"] = False
      print('op head') 
    """

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

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    # food = game_state['board']['food']

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({
        "info": info, 
        "start": start, 
        "move": move, 
        "end": end
    })
