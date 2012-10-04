from itertools import *
from src.filter import *
from src.pool.transforms import transformation_pool

def fetch_pools(grid, direction):
  """
  The outside face of the pool module. Given the grid, return the different
  pool configurations that makes sense.

  @return A list with 3 elements, each element is a pair of a list of Filters
  """
  def get_fig_pair(ix_pair):
    y0, x0 = ix_pair[0]
    y1, x1 = ix_pair[1]
    return [grid[y0][x0], grid[y1][x1]]

  arrows = positions(len(grid), direction)
  return create_pool(imap(get_fig_pair, arrows))

def create_pool(figure_pairs):
  """
  Given a list of figure-pairs, return a list of Filters that are sensible
  based on the inputs. This method will use the analogy understanding
  logic imported from the other files across this module. Furthermore, this
  method will do filtering to ensure that the filters at least accept the input
  """
  figure_pairs = list(figure_pairs)
  accept_all_filter = Filter(lambda old, new: True, 99999999, "No pattern")
  works = lambda f: all(imap(lambda fig_pair: f.accept(*fig_pair),
    figure_pairs))
  return ifilter(works,
    chain(transformation_pool(figure_pairs),
    [accept_all_filter]))

def positions(n, direction):
  dy, dx = direction
  last = (n-1, n-1)
  for y0 in range(n):
    for x0 in range(n):
      x = x0 + dx
      y = y0 + dy
      if dy > 0 and dx > 0:
        y %= n
      res = ((y0, x0), (y, x))
      if last not in res and y < n and x < n:
        yield res

def positionss(n, directions):
  """
  Get all the two lists of "positions" yielded by using the directions that
  should be linearly independent
  """
  positionsn = lambda d: positions(n, d)
  return imap(positionsn, directions)
