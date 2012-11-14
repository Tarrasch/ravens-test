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
###
from reshape import reshape_images
from transformations import transformations

def s(img): pl.imshow(img); pl.gray(); pl.show()

def solve(tree):
  v = solve_very_verbose(tree)
  return [extract(v), extract_verbose(v), v]

def extract(solution):
  return extract_verbose(solution)[2]

def extract_verbose(solution):
  return max(solution)

def solve_very_verbose(tree):
  return list(solve_very_verbose_(tree))

def solve_very_verbose(tree):
  return list(solve_very_verbose_(tree))

def solve_very_verbose_(tree):
  # s(tree[3])
  tree = reshape_images(tree)
  # s(tree[3])
  grid = tree["grid"]
  alternatives = tree.keys()
  alternatives.remove("grid")
  for alternative in sorted(alternatives):
    alt_image = tree[alternative]
    def try_tranformation(t):
      f, desc = t
      score = f(grid, alt_image)
      return (score, desc, alternative)

    yield max(map(try_tranformation, transformations()))
