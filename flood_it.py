"""A raucous ripoff of Flood-It! 2, a game I liked to play on my iphone.
"""


import random
import sys


BOARD_SIDELENGTH = 12
N_TURNS = 22


class Color(object):

  COLORS = [
      "purple",
      "pink",
      "orange",
      "yellow",
      "green",
      "blue"
      ]

  def __init__(self, color):
    if self.validate_color(color):
      self.color = color
    else:
      raise ValueError('Invalid color {0}'.format(color))

  @classmethod
  def random_color(cls):
    return random.choice(cls.COLORS)

  @classmethod
  def validate_color(cls, color):
    return color in cls.COLORS


class Tile(object):

  def __init__(self, color=None):
    """If no color is provided, a random color is generated."""
    if color:
      self.color = color
    else:
      self.color = Color.random_color()


class Board(object):

  def __init__(self, sidelength, flooded_tiles=None):
    """Initializes a sidelength-by-sidelength board of Tiles."""
    self.board = [
        [Tile() for _ in range(sidelength)]
        for _ in range(sidelength)
        ]

    if flooded_tiles:
      self.flooded_tiles = flooded_tiles
    else:
      self.flooded_tiles = {self.board[0][0]}  # Start with the top left tile

    self._sidelength = sidelength
    self._num_tiles = sidelength**2

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
    self.flooded_tiles = self.flooded_tiles.union(
        self.flood(color)
        )
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
        neighbor for neighbor in self.find_neighbors(self.flooded_tiles)
        if neighbor.color == new_color
        }

  def find_neighbors(self, flooded_tiles):
    """Finds all tiles adjacent to the provided flooded_tiles."""
    neighbors = []
    for x in range(self._sidelength):
      for y in range(self._sidelength):
        pass

    return []  # FIXME


def main():
  # Construct board
  board = Board(BOARD_SIDELENGTH)

  for turn in range(N_TURNS):
    color = get_color('Flood Color: ')
    board.play(color)
    if won(turn, board):
      print_gameover_info(turn, board)

  # Otherwise, the player lost
  print_gameover_info(turn, board)


def won(turns, board):
  """Returns True if the game is in a win state."""
  return turns < N_TURNS and board.is_flooded()


def get_color(prompt=''):
  """Get the flood color for this round from the user."""
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


if __name__ == '__main__':
  main()
