import itertools
from pprint import pprint

def make_subfig(yx, d={}):
  y, x = yx
  res = { "x": x*15, "y": y*15 }
  res.update(d)
  return res

def make_fig(y, x):
  d = { "rot": y*180+x*180-180*3 }
  my_make_subfig = lambda yx: make_subfig(yx, d=d)
  return map(my_make_subfig, itertools.product(range(y+1), range(x+1)))


y_max = 3
x_max = 3
res = [ [make_fig(y, x) for x in range(x_max)] for y in range(y_max)]
pprint(res)
