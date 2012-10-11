from itertools import *
from pprint import pprint

def make_fig(n):
  lists = chain([[0, 0]],
                zip(range(1,n),repeat(0)),
                zip(repeat(0), range(1,n)),
                zip(repeat(0), range(-n+1, 0)))
  return [{"x": x, "y": y} for y, x in lists]

grid = [[make_fig(x-y+3) for x in range(3)] for y in range(3)]
grid[2].pop()

di= {k: make_fig(k) for k in range(1,6)}
di.update({"grid": grid})

pprint(di)
