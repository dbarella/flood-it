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


def main():
  # Construct board
  board = construct_board(BOARD_SIDELENGTH)
  flooded_tiles = set(board[0][0])  # Start with the top left tile

  for turn in range(N_TURNS):
    color = get_color('Flood Color:')
    flooded_tiles = play(color, flooded_tiles, board)
    if board_flooded(flooded_tiles, board):  # Win condition
      print_gameover_info(turn, flooded_tiles, board, won=True)

  # Otherwise, the player lost
  print_gameover_info(turn, flooded_tiles, board, won=False)


def construct_board(sidelength):
  """Returns a sidelength-by-sidelength board of Tiles."""
  return [
      [Tile() for _ in range(sidelength)]
      for _ in range(sidelength)
      ]


def board_flooded(flooded_tiles, board):
  """Returns True if the board is flooded, false otherwise."""
  return len(flooded_tiles) == BOARD_SIDELENGTH**2


def won(turns, flooded_tiles, board):
  """Returns True if the game is in a win state."""
  return board_flooded(flooded_tiles, board) and turns < N_TURNS


def play(color, flooded_tiles, board):
  """
  Plays for a round, returning the set of currently flooded tiles.

  Args:
    color (Color): The color with which to flood the board this round
    flooded_tiles (set of Tile): The set of flooded tiles
    board (list of (list of Tile)): The game board
  Returns (set of Tile):
    Returns the new set of flooded tiles.
  """
  return flooded_tiles.union(
      flood(color, flooded_tiles, board)
      )


def flood(color, flooded_tiles, board):
  """
  Floods the board with a color, returning the resulting set of flooded tiles.

  Args:
    color (Color): The color with which to flood the board this round
    flooded_tiles (set of Tile): The set of flooded tiles
    board (list of (list of Tile)): The game board
  Returns (set of Tile):
    Returns the new set of flooded tiles.
  """
  return {
      neighbor for neighbor in find_neighbors(flooded_tiles, board)
      if neighbor.color == new_color
      }


def find_neighbors(flooded_tiles, board):
  """Finds all tiles adjacent to the currently flooded tiles."""
  neighbors = []
  for x in range(BOARD_SIDELENGTH):
    for y in range(BOARD_SIDELENGTH):

  return []  # FIXME


def get_color(prompt=''):
  """Get the flood color for this round from the user."""
  user_color = raw_input(prompt)
  while not Color.validate_color(user_color):
    print "THAT AIN'T A VALID COLOR"
    user_color = raw_input(prompt)

  return Color(user_color)


def print_gameover_info(turns, flooded_tiles, board, won=False):
  if won:
    print 'You won.'
  else:
    print 'Nah you lost.'


if __name__ == '__main__':
  main()
