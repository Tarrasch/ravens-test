from itertools import *
import operator
import cv2
from itertools import *
import numpy
import numpy as np
import scipy
import pylab as pl
import pylab
import pymorph
from scipy import misc
from pprint import pprint
import operator
import copy
from similarity import similarity

def s(img): pl.imshow(img); pl.gray(); pl.show()

# Let a transformation be a tuple:
#
# (f, desc)
#
# where desc is a string description and f(grid, alt) is a real value judgement
# of how well the transformation applies. 1.0 = perfect, 0 = not at all
#

def applyN(fun, n):
  return reduce(lambda f1, f2: lambda x: f1(f2(x)), [fun]*n, lambda x: x)

def prod_root(*xs):
  return numpy.array(xs).prod()**(1.0/len(xs))

def transformations():
  return [
      (t2d(lambda x: x), "identity-transformer"),
      (t2d(mirror_x), "mirror x"),
      (t2d(applyN(np.rot90, 1)), "rotate by 90"),
      (t2d(applyN(np.rot90, 2)), "rotate by 180"),
      (t2d(applyN(np.rot90, 3)), "rotate by 270"),
      (xor_rows_then_compare, "xor rows then compare"),
      (xor_cands_then_pix_count, "xor cands then pix count"),
  ]

# Given an image modifier, check how much the 2 by 2-ification of the grid
# obeys that modifier
def t2d(modifier):
  def fun(grid, alt):
    n = len(grid)
    tl, tr, bl, br = grid[0][n-2], grid[0][n-1], grid[n-1][n-2], alt
    s_top = similarity(modifier(tl), tr)
    s_bot = similarity(modifier(bl), br)
    # return min(s_top, s_bot)
    return s_top * s_bot
  return fun

def mirror_x(img):
  new = np.copy(img)
  sz = img.shape[0]
  sz2 = sz/2
  new[:,np.arange(sz2+sz2-1,sz2-1,-1)] = img[:,0:sz2]
  return new

def xor_rows_then_compare(grid, alt):
  if(len(grid) == 2):
      return 0
  grid = copy.deepcopy(grid)
  grid[2].append(alt)
  top = reduce(lambda a, b: a^b, grid[0])
  bot = reduce(lambda a, b: a^b, grid[2])
  a_top = reduce(lambda a, b: a&b, grid[0], top)
  a_bot = reduce(lambda a, b: a&b, grid[2], bot)
  top_xor = pymorph.open(top^a_top)
  bot_xor = pymorph.open(bot^a_bot)
  return similarity(top_xor, bot_xor)

def xor_cands_then_pix_count(grid, alt):
  if(len(grid) == 2):
      return 0
  n = len(grid)
  tl, tr, bl, br = grid[0][n-2], grid[0][n-1], grid[n-1][n-2], alt
  l = tl^bl
  r = tr^br
  v1, v2 = l.sum()*3.0, r.sum()*2.0
  return min(v1, v2)/(max(v1, v2)+1)
