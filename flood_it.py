#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A raucous ripoff of Flood-It! 2, a game I like to play on my iPhone.
"""


from termcolor import colored

import os
import pprint
import random


BOARD_WIDTH  = 12
BOARD_HEIGHT = 12
N_TURNS      = 22


class Color(object):

  COLORS = (
      'r',
      'c',
      'm',
      'y',
      'g',
      'b'
      )

  COLORS_TO_OUTPUT = {
      'r' : colored(' R ', 'red'    , attrs=['bold', 'reverse']),
      'c' : colored(' C ', 'cyan'   , attrs=['bold', 'reverse']),
      'm' : colored(' M ', 'magenta', attrs=['bold', 'reverse']),
      'y' : colored(' Y ', 'yellow' , attrs=['bold', 'reverse']),
      'g' : colored(' G ', 'green'  , attrs=['bold', 'reverse']),
      'b' : colored(' B ', 'blue'   , attrs=['bold', 'reverse'])
      }

  def __init__(self, color=None):
    if not color:
      self.color = self.random_color()
    elif self.validate_color(color):
      self.color = color
    else:
      raise ValueError('Invalid color {0}'.format(color))

  def __str__(self):
    return self.COLORS_TO_OUTPUT[self.color]

  def __repr__(self):
    return repr(self.color)

  def __eq__(self, other):
    if type(self) is type(other):
      return self.color == other.color
    else:
      return False

  @classmethod
  def random_color(cls):
    """Returns a random color name."""
    return random.choice(cls.COLORS)

  @classmethod
  def validate_color(cls, color):
    return color in cls.COLORS


class Tile(object):

  def __init__(self, x, y, color=None):
    """If no color is provided, a random color is generated."""
    self.x = x
    self.y = y

    if color:
      self.color = color
    else:
      self.color = Color()

  def __str__(self):
    return str(self.color)

  def __repr__(self):
    return repr('{0} at ({1}, {2})'.format(self.color, self.x, self.y))

  def flood(self, color):
    """Floods this tile with a color (mostly sugar, otherwise just a setter)"""
    self.color = color


class Board(object):

  def __init__(self, width, height):
    """Initializes a width-by-height board of Tiles."""
    self._width  = width
    self._height = height
    self._num_tiles = width * height

    self.board = [
        [Tile(x, y) for x in range(width)]
        for y in range(height)
        ]

    # Start with the top left tile
    starting_tile = self.board[0][0]
    self.flooded_tiles = {starting_tile}
    self.flooded_tiles.update(self.find_floodplane(starting_tile.color))

  def __len__(self):
    return self._num_tiles

  def is_flooded(self):
    """Returns True if the board is flooded, false otherwise."""
    return len(self.flooded_tiles) == self._num_tiles

  def flood(self, color):
    """
    Plays for a round of the game.

    !!MUTATES BOARD STATE!!

    Args:
      color (Color): The color with which to flood the board this round
    """
    # Change current flood plane to the new flood color (start flooding)
    for tile in self.flooded_tiles:
      tile.flood(color)

    # This statement does not mutate the board state.
    new_flooded_tiles = self.find_floodplane(color)

    # Modify board state to include the newly flooded tiles (finish flooding)
    self.flooded_tiles.update(new_flooded_tiles)

  def find_floodplane(self, color):
    """
    Returns the result of flooding the board with a certain color.

    !!Does NOT mutate board state!!

    Runs a BFS starting with the flooded tiles

    Args:
      color (Color): The color with which to flood the board this round

    Returns (set of Tile):
      The new set of flooded tiles.
    """
    # Initialize the BFS queue with the top-left tile
    queue = [ self.board[0][0] ]

    flooded_tiles = set()

    while queue:
      tile = queue.pop()

      # If the color of the tile matches the flooding color, add it
      if tile.color == color:
        flooded_tiles.add(tile)

        # Add the tile's unflooded neighbors
        queue.extend(
              [neighbor for neighbor in self.safe_get_neighbors(tile)
               if neighbor not in flooded_tiles]
            )

    return flooded_tiles


  def safe_get_neighbors(self, tile):
    """Safe neighbor lookup for a tile; handles the edge cases and all."""
    neighbors = []

    # Look at North, South, East, West neighbors (x, y)
    for x_offset, y_offset in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
      # Do the index calculation upfront to avoid redoing it in the 'if'
      tmp_x = tile.x + x_offset
      tmp_y = tile.y + y_offset
      if (0 <= tmp_x < self._width and 0 <= tmp_y < self._height):
        neighbors.append(self.board[tmp_y][tmp_x])  # [row][column] resolution

    return neighbors

  def display(self):
    """
    Custom display method, let the board display itself.

    This should eventually be delegated to a standalone display method.
    """
    for row in self.board:
      print ''.join('{0:3}'.format(str(tile)) for tile in row)


def blit():
  """Blit the screen"""
  # Blit the screen
  _ = os.system('clear')


def won(turns, board):
  """Returns True if the game is in a win state."""
  return turns < N_TURNS and board.is_flooded()


def get_color(prompt=''):
  """Get the flood color for this round from the user."""
  print 'Color options: {0}'.format(Color.COLORS)

  user_color = raw_input(prompt).lower()
  while not Color.validate_color(user_color):
    print "THAT AIN'T A VALID COLOR"
    user_color = raw_input(prompt)

  return Color(user_color)


def print_gameover_info(turns, board):
  if won(turns, board):
    print 'You won.'
  else:
    print 'Nah, you lost.'


def print_game_stats(turn, board):
  print 'Turn {0:3d} of {1:3d}'.format(turn, N_TURNS)


def main():
  # Clear the screen for the game.
  blit()

  # Construct board
  board = Board(width=BOARD_WIDTH, height=BOARD_HEIGHT)

  # Display the board
  board.display()

  for turn in range(N_TURNS):

    print_game_stats(turn, board)

    # Play a round
    board.flood( get_color('Flood Color: ') )

    blit()
    board.display()

    # Terminate early on a win
    if won(turn, board):
      break

  print_gameover_info(turn, board)


if __name__ == '__main__':
  main()
