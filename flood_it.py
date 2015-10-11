"""A raucous ripoff of Flood-It! 2, a game I liked to play on my iphone.
"""


import random


BOARD_SIDELENGTH = 12
N_TURNS = 22


class Tile(object):

  COLORS = [
      "purple",
      "pink",
      "orange",
      "yellow",
      "green",
      "blue"
      ]

  def __init__(self):
    self.color = random.choice(Tile.COLORS)


def main():
  # Construct board
  board = construct_board(BOARD_SIDELENGTH)
  flooded_tiles = set()

  # While not over, play
  # while not board_flooded(flooded_tiles, board) and turns < N_TURNS:  # TODO: Refactor into game object
    # flooded_tiles = play(flooded_tiles, board)

    # # Ugly...
    # turns += 1

  for turn in range(N_TURNS):
    if board_flooded(flooded_tiles, board):
      break
    else:
      flooded_tiles = play(flooded_tiles, board)

  # Talk about the end of the game
  print_gameover_info(turn, flooded_tiles, board)


def construct_board(sidelength):
  """Returns a sidelength-by-sidelength board of Tiles."""
  return [
      [Tile() for _ in range(sidelength)]
      for _ in range(sidelength)
      ]

def board_flooded(flooded_tiles, board):
  return len(flooded_tiles) == BOARD_SIDELENGTH**2


def play(flooded_tiles, board):
  neighbors = {
      neighbor for neighbor in find_neighbors(flooded_tiles, board)
      if neighbor.color == new_color
      }
  return flooded_tiles.union(neighbors)


def find_neighbors(flooded_tiles, board):
  return []  # FIXME


def won(turns, flooded_tiles, board):
  return board_flooded(flooded_tiles, board) and turns < N_TURNS


def print_gameover_info(turns, flooded_tiles, board):
  if won(turns, flooded_tiles, board):
    print 'You won.'
  else:
    print 'Nah you lost.'


if __name__ == '__main__':
  main()
