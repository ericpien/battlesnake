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
import pandas as pd


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
      safe_moves = ['up','down','left','right']
      
    

  
    moves = []
    scores = []
    summary = pd.DataFrame()
    
    for move in safe_moves:
        step_2_lob = []
        step_3_lob = []      
      
        for b in next_lob(game_state['board'], [], 0, move):
            my_snake = [snake for snake in b['snakes'] if snake['name'] == snake_name]
            
            if len(my_snake) > 0:
              lohazard = b['hazards']
              lobody = sum([sn['body'][:-1] for sn in b['snakes']],[])
              lowall = []
              for h in range(board_height+1):
                  lowall.append({"x":-1, "y":h})
                  lowall.append({"x":board_width, "y":h})
              
              for w in range(board_width+1):
                  lowall.append({"x":w, "y":-1})
                  lowall.append({"x":w, "y":board_height})
              
              lodanger = (lohazard + lobody + lowall)

              next_pos = my_snake[0]["head"]
              next_moves = [{'move': 'left', 'pos': {"x": next_pos["x"]-1, "y": next_pos["y"]}},
                  {'move': 'right', 'pos': {"x": next_pos["x"]+1, "y": next_pos["y"]}},
                  {'move': 'down', 'pos': {"x": next_pos["x"], "y": next_pos["y"]-1}},
                  {'move': 'up', 'pos': {"x": next_pos["x"], "y": next_pos["y"]+1}}]

              safe_next_moves = [m['move'] for m in next_moves if m['pos'] not in lodanger]
              unsafe_next_moves = [m['move'] for m in next_moves if m['pos'] in lodanger]

              if len(safe_next_moves) == 0:
                safe_next_moves = unsafe_next_moves
              
              for move2 in safe_next_moves:
                step_2_lob += next_lob(b, [], 0 , move2) 
                

              
        score = [score_b(b) for b in step_2_lob]
    
        if len(score) > 0:
            moves.append(move)
            scores.append(mean(score))
        
    summary["moves"] = moves
    summary["scores"] = scores

    print(summary)
  

    if len(summary) == 0:
      print("No safe moves detected! Going rogue")
      next_move = random.choice(safe_moves)
      
      return {"move": next_move}
      
    max_score = max(summary['scores'])
    best_next_moves = []
    for i in range(len(summary)):
      if summary['scores'][i] == max_score:
          best_next_moves.append(summary['moves'][i])
    
    safe_moves = best_next_moves
    print('available moves are: {}'.format(safe_moves))
      

  
  
  # Move towards food
    food = game_state['board']['food'] #array of (x,y) [{"x":, "y": }]

    if len(food) == 0:
      next_move = random.choice(safe_moves)
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



from statistics import mean

def score_b(board):
    my_snake = [snake for snake in board['snakes'] if snake['name'] == snake_name]
    los_excl_self = board['snakes'].copy()
    
  
    #death_aversion: am i alive
    death_aversion = 0
    hunger_aversion = 0
    agression = 0

    if len(my_snake) == 0:
      death_aversion = -1000
    elif len(my_snake) == 1:
      hunger_aversion = 1000 * my_snake[0]['length']
      los_excl_self.remove(my_snake[0])
      agression = -1000 * len(los_excl_self)
    
    #distance to food: the closer the better
    distance = 0
    

    factors = [death_aversion, distance, agression, hunger_aversion]
    score = mean(factors)
    return score
  
def euclidean_distance(coord1, coord2):
    n = math.sqrt((coord1["x"]-coord2["x"])**2 + (coord1["y"]-coord2["y"])**2)
    return n

def next_lob(board, lolos, counter, branch):
    # board: board object
    # lolos: running list of snakes  #listof (listof snakes)
    # counter: counter for each recursive loop
    # branch: indicates my snake's moves. one of: 'left' 'right' 'up' 'down'
    
    # PULL ITEMS OUT OF THE BOARD OBJECT
    snakes = board["snakes"]             # listof [sn, sn, ...] - list of snakes on the board
    snake = snakes[counter:counter+1][0] # [{"id": , ... }.{"id": , ...}] - snake which is going to be making the turn
    hazards = board["hazards"]           # listof [({'x':_,'y':_}),...] - list of coordinates of hazards
    board_height = board["height"]       # Natural
    board_width = board["width"]         # Natural
    foods = board["food"]                # listof [({'x':_,'y':_}),...] - list of coordinates of foods
    
    # INITIATE MOVE
    # lolop_all4 is listof (listof {x,y})
    # lolop_all4 represents all of the next possible moves for a given snake
    # if the snake is my snake, it will simply generate the specific safe move as represented by branch
    lolop_all4 = []

    if (snake['name'] ==  snake_name):
        if branch == 'up':
            lolop_all4.append([{"x": snake['head']['x'] , "y": snake['head']['y']+1}] + snake['body'][:])
        elif branch == 'down':
            lolop_all4.append([{"x": snake['head']['x'] , "y": snake['head']['y']-1}] + snake['body'][:])
        elif branch == 'left':
            lolop_all4.append([{"x": snake['head']['x']-1, "y": snake['head']['y']}] + snake['body'][:])
        elif branch == 'right':
            lolop_all4.append([{"x": snake['head']['x']+1, "y": snake['head']['y']}] + snake['body'][:])

    else: lolop_all4 = [
            [{"x": snake['head']['x'] , "y": snake['head']['y']+1}] + snake['body'][:],
            [{"x": snake['head']['x'] , "y": snake['head']['y']-1}] + snake['body'][:],
            [{"x": snake['head']['x']-1 , "y": snake['head']['y']}] + snake['body'][:],
            [{"x": snake['head']['x']+1 , "y": snake['head']['y']}] + snake['body'][:]
        ]
    
    # HAZARD / OUT OF BOUNDS / IMPLODE
    # lolop is a listof (listof {x,y})
    # lolop screens out any snakes that have hit a hazard or is out of bounds
    lolop = []
    for p in lolop_all4:
        if (not ((p[0] in hazards) or
            (p[0]['x'] < 0) or
            (p[0]['x'] > (board_width - 1)) or 
            (p[0]['y'] < 0) or
            (p[0]['y'] > (board_height - 1)) or
            (p[0] in p[1:]))):

            lolop.append(p)

    # FOOD
    # lolop_food_adj is a listof (listof {x,y})
    # foods_not_eaten is a listof {x,y}
    # lolop_food_adj includes snakes adjusted for whether it ate a food or not
    # foods_not_eaten is foods, with eaten foods removed 
    lolop_food_adj = []
    foods_not_eaten = foods
    for p in lolop:
        if p[0] in foods:
            lolop_food_adj.append(p)
        else:
            lolop_food_adj.append(p[:-1])
        
    for f in foods:
        for p in lolop:
            if f in p:
                foods_not_eaten.remove(f)

    # CONVERT POSITION TO SNAKE DATA
    # lolop_to_lolos is a listof (listof snakes)
    # lolop_to_lolos takes lolop_food_adj and produce list of list of snakes
    lolop_to_lolos = []
    for pos in lolop_food_adj:
        lolop_to_lolos.append(
            [{
                "id": snake['id'],
                "name": snake['name'],
                "health": 54,
                "body": pos,
                "latency": snake['latency'],
                "head": pos[0],
                "length": len(pos),
                "shout": snake['shout'],
                "squad": snake['squad'],
                "customizations": snake['customizations']
            }]
        )

    # APPEND NEW SNAKE TO OLD LISTOF SNAKES
    # next_lolos is a listof (listof snake)
    # append new snakes to old list of snakes
    next_lolos = [] #[[sn, sn, ...], [sn, sn, ...], [sn, sn, ...]]

    if len(lolos) == 0:
        next_lolos = lolop_to_lolos
    else:    
        for los in lolos:                           #starting list
            losb = []
            for s in los:                           #each snake already processed
                losb.append(s['body'])              #add to listof snake bodies
                
            for s in lolop_to_lolos:                #new snake
                if (s[0]['head'] not in losb[0]):   #append if not collided
                    next_lolos.append(los + s)


    # TEST OF RECURSION
    # basecase condition: if we have looped through every snake on the board
    # convert the list of snakes to board representations
    # and return the board
    counter += 1
    if counter == len(snakes):
        lob = []
        for los in next_lolos:
            lob.append(
                {"height": board_height,
                "width": board_width,
                "food": foods_not_eaten,
                "hazards": hazards,
                "snakes": los 
                }
            )
        return lob

    # Trust the natural recursion <3
    return next_lob(board, next_lolos, counter, branch)
  
# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({
        "info": info, 
        "start": start, 
        "move": move, 
        "end": end
    })
