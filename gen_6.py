import itertools
from pprint import pprint

def make_subfig(yx):
  y, x = yx
  return { "x": x*15, "y": y*15 }

def make_fig(y, x):
  return map(make_subfig, itertools.product(range(y+1), range(x+1)))


y_max = 3
x_max = 3
res = [ [make_fig(y, x) for x in range(x_max)] for y in range(y_max)]
pprint(res)
