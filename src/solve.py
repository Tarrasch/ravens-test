from itertools import *
from directions import std_directions, lid_directionss, direction_mnemonic
from pool.pool import fetch_pools
from src.filter import select_best_filter
import operator

def solve(tree):
  return min(solve_verbose(tree), key=operator.itemgetter(2))[0]

def solve_verbose(tree):
  grid = tree["grid"]
  filterss = get_filterss(grid) # Only to memoize it
  alternatives = tree.keys()
  alternatives.remove("grid")
  for alternative in alternatives:
    alt_image = tree[alternative]
    def judge_directions(directions):
      dir_filterss = map(lambda dir: filterss[dir], directions)
      filter_pair = [select_best_filter(filterss[dir], get_from_figure(grid, dir), alt_image)
                        for dir in directions]
      total_cost = sum(map(lambda f: f.punishment, filter_pair))
      return (alternative, zip(filter_pair, map(direction_mnemonic, directions)), total_cost)

    yield max(map(judge_directions, lid_directionss()), key=operator.itemgetter(2))

def get_filterss(grid):
  """
  Given a grid, get a list of filters by considering analogies form each direction,
  that is, one element per direction
  """
  return dict((dir, fetch_pools(grid, dir)) for dir in std_directions())

def get_from_figure(grid, direction):
  """
  Get the figure that would go to the last figure if you use given direction
  """
  n = len(grid)
  y0, x0 = n-1-direction[0], n-1-direction[1]
  return grid[y0][x0]
