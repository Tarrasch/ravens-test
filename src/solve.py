from itertools import *
from directions import std_directions, lid_directionss, direction_mnemonic
from pool.pool import fetch_pools
from src.filter import select_best_filter
import operator

def solve(tree):
  v = solve_very_verbose(tree)
  return [extract(v), extract_verbose(v), v]

def extract(solution):
  return extract_verbose(solution)[0]

def extract_verbose(solution):
  return min(solution, key=operator.itemgetter(2))

def solve_very_verbose(tree):
  return list(solve_very_verbose_(tree))

def solve_very_verbose_(tree):
  grid = tree["grid"]
  filterss = get_filterss(grid) # Only to memoize it
  alternatives = tree.keys()
  alternatives.remove("grid")
  for alternative in sorted(alternatives):
    alt_image = tree[alternative]
    def judge_directions(directions):
      dir_filterss = map(lambda dir: filterss[dir], directions)
      filter_pair = [select_best_filter(filterss[dir], get_from_figure(grid, dir), alt_image)
                        for dir in directions]
      total_cost = sum(map(lambda f: f.punishment, filter_pair))
      return (alternative, zip(filter_pair, map(direction_mnemonic, directions)), total_cost)

    yield min(map(judge_directions, lid_directionss()), key=operator.itemgetter(2))

def get_filterss(grid):
  """
  Given a grid, get a list of filters by considering analogies form each direction,
  that is, one element per direction
  """
  # Implementation detail: eh... we have to list the result since we cache it
  return dict((dir, list(fetch_pools(grid, dir))) for dir in std_directions())

def get_from_figure(grid, direction):
  """
  Get the figure that would go to the last figure if you use given direction
  """
  n = len(grid)
  y0, x0 = n-1-direction[0], n-1-direction[1]
  return grid[y0][x0]
