import math

# Represent X and Y coordinates and perform operations on them
class Coordinate:

  # Coordinate has these constants for quick operations
  LEFT =  {'x': -1, 'y':  0}
  RIGHT = {'x':  1, 'y':  0}
  UP =    {'x':  0, 'y':  1}
  DOWN =  {'x':  0, 'y': -1}

  # Initialize coordinate using a dictionary {'x': int, 'y': int}
  def __init__(self, xy: dict):
    self.x = xy['x']
    self.y = xy['y']

  # Add current coordinate to coord and return new coordinate
  def __add__(coord1:"Coordinate", coord2: "Coordinate") -> "Coordinate":
    return Coordinate({'x':coord1.x + coord2.x, 'y':coord1.y + coord2.y})

  # Print Coordinate (x,y)
  def __str__(self):
    return "('x': {}, 'y' {})".format(self.x, self.y)

  # two coordinates are equal if the x and y are equal
  def __eq__(self, other):
    return isinstance(other, Coordinate) and (self.x == other.x and self.y == other.y)

  # make the class hashable
  def __hash__(self):
      return hash((self.x, self.y))

  # Move coordinate point one LEFT
  def move_left(self) -> "Coordinate":
    return Coordinate({
      'x': self.x + self.LEFT['x'],
      'y': self.y + self.LEFT['y']
    })

  # Move coordinate point one RIGHT
  def move_right(self) -> "Coordinate":
    return Coordinate({
      'x': self.x + self.RIGHT['x'],
      'y': self.y + self.RIGHT['y']
    })

  # Move coordinate point one UP
  def move_up(self) -> "Coordinate":
    return Coordinate({'x': self.x + self.UP['x'], 'y': self.y + self.UP['y']})

  # Move coordinate point one DOWN
  def move_down(self) -> "Coordinate":
    return Coordinate({
      'x': self.x + self.DOWN['x'],
      'y': self.y + self.DOWN['y']
    })

  def euclidean_distance(coord1: dict, coord2: dict) -> float:
    if isinstance(coord1, Coordinate):
      coord1 = {"x": coord1.x, "y": coord1.y}

    if isinstance(coord2, Coordinate):
      coord2 = {"x": coord2.x, "y": coord2.y}

    # Return the euclidean distance from current coordinate to coord2
    n = math.sqrt((coord1['x'] - coord2['x'])**2 +
                  (coord1['y'] - coord2['y'])**2)
    return n
  
