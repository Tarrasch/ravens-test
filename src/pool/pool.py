from itertools import *

def fetch_pools(grid):
  """
  The outside face of the pool module. Given the grid, return the different
  pool configurations that makes sense.

  @return A list with 3 elements, each element is a pair of a list of Filters
  """
  def get_fig_pair(ix_pair):
    y0, x0 = ix_pair[0]
    y1, x1 = ix_pair[1]
    return [grid[y0][x0], grid[y1][x1]]

  def extract(arrows):
    return create_pool(imap(get_fig_pair, arrows))

  return imap(lambda lid_pair: imap(extract, lid_pair), lid_positions(len(grid)))

def create_pool(figure_pairs):
  """
  Given a list of figure-pairs, return a list of Filters that are sensible
  based on the inputs. This method will use the analogy understanding
  logic imported from the other files across this module.
  """
  print "Not Implemented: create_pool!!!"
  return []

# Hooray for completely pure functions!
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


def lid_positions(n):
  """
  Get all the two lists of "positions" yielded by using two directions that
  are linearly independent
  """
  positionsn = lambda d: positions(n, d)
  directionss = combinations([(1, 0), (0, 1), (1, 1)], 2)
  return imap(lambda x: imap(positionsn, x), directionss)
