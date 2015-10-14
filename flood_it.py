#!/usr/bin/env python
 # -*- coding: utf-8 -*-

"""A raucous ripoff of Flood-It! 2, a game I liked to play on my iphone.
"""


import os
import pprint
import random
import sys
from termcolor import colored


BOARD_WIDTH  = 12
BOARD_HEIGHT = 12
N_TURNS      = 22


class Color(object):

  COLORS = [
      "red",
      "cyan",
      "red",
      "yellow",
      "green",
      "blue"
      ]

  COLORS_TO_OUTPUT = {
      "red"     : colored(' R ', 'red'    , attrs=['bold', 'reverse']),
      "cyan"    : colored(' C ', 'cyan'   , attrs=['bold', 'reverse']),
      "magenta" : colored(' M ', 'magenta', attrs=['bold', 'reverse']),
      "yellow"  : colored(' Y ', 'yellow' , attrs=['bold', 'reverse']),
      "green"   : colored(' G ', 'green'  , attrs=['bold', 'reverse']),
      "blue"    : colored(' B ', 'blue'   , attrs=['bold', 'reverse'])
      }

  def __init__(self, color=None):
    if not color:
      self.color = self.random_color()
    elif self.validate_color(color):
      self.color = color
    else:
      raise ValueError('Invalid color {0}'.format(color))

  @classmethod
  def random_color(cls):
    """Returns a random color name."""
    return random.choice(cls.COLORS)

  @classmethod
  def validate_color(cls, color):
    return color in cls.COLORS

  def __str__(self):
    return self.COLORS_TO_OUTPUT[self.color]

  def __eq__(self, other):
    if type(self) is type(other):
      return self.color == other.color
    else:
      return False


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


class Board(object):

  def __init__(self, width, height, flooded_tiles=None):
    """Initializes a width-by-height board of Tiles."""
    self._width  = width
    self._height = height
    self._num_tiles = width * height

    self.board = [
        [Tile(x, y) for x in range(width)]
        for y in range(height)
        ]

    if flooded_tiles:
      self.flooded_tiles = flooded_tiles
    else:
      self.flooded_tiles = {self.board[0][0]}  # Start with the top left tile

  def __len__(self):
    return self._num_tiles

  def is_flooded(self):
    """Returns True if the board is flooded, false otherwise."""
    return len(self.flooded_tiles) == self._num_tiles

  def play(self, color):
    """
    Plays for a round, returning the set of currently flooded tiles.

    !!MUTATES BOARD STATE!!

    Args:
      color (Color): The color with which to flood the board this round
    Returns (set of Tile):
      Returns the new set of flooded tiles.
    """
    # This statement does not mutate any state.
    new_flooded_tiles = self.flood(color)

    # Mutate board state
    self.flooded_tiles = self.flooded_tiles.union(new_flooded_tiles)

    # Mutate tile state, watch out
    for tile in self.flooded_tiles:
      tile.color = color

    return self.flooded_tiles

  def flood(self, color):
    """
    Returns the result of flooding the board with a certain color.

    !!Does NOT mutate board state!!

    Args:
      color (Color): The color with which to flood the board this round
    Returns (set of Tile):
      Returns the new set of flooded tiles.
    """
    return {
        neighbor for neighbor in self.tiles_adjacent_to(self.flooded_tiles)
        if neighbor.color == color
        }

  def tiles_adjacent_to(self, flooded_tiles):
    """Finds all tiles adjacent to flooded_tiles."""
    neighbors = set()

    for x, row in enumerate(self.board):
      for y, tile in enumerate(row):
        if tile in flooded_tiles:
          neighbors.update(self.safe_get_neighbors(tile))

    return neighbors

  def safe_get_neighbors(self, tile):
    """Safe neighbor lookup for a tile; handles the edge cases and all."""
    neighbors = []

    # Look at North, South, East, West neighbors (x, y)
    for x_offset, y_offset in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
      # Do the index calculation upfront to avoid redoing it in the 'if'
      tmp_x = tile.x + x_offset
      tmp_y = tile.y + y_offset
      if (0 <= tmp_x < self._width and 0 <= tmp_y < self._height):
        neighbors.append(self.board[tmp_x][tmp_y])

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

  user_color = raw_input(prompt)
  while not Color.validate_color(user_color):
    print "THAT AIN'T A VALID COLOR"
    user_color = raw_input(prompt)

  return Color(user_color)


def print_gameover_info(turns, board):
  if won(turns, board):
    print 'You won.'
  else:
    print 'Nah you lost.'


def main():
  # Clear the screen for the game.
  blit()

  # Construct board
  board = Board(width=BOARD_WIDTH, height=BOARD_HEIGHT)

  for turn in range(N_TURNS):
    blit()

    # Display the board
    board.display()

    # Play a round
    board.play( get_color('Flood Color: ') )

    # Terminate early on a win
    if won(turn, board):
      break

  print_gameover_info(turn, board)


if __name__ == '__main__':
  main()
