from itertools import *
from reshape import reshape_images
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

def s(img): pl.imshow(img); pl.gray(); pl.show()

def solve(tree):
  s(tree[3])
  tree = reshape_images(tree)
  s(tree[3])
  grid = tree["grid"]
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

    return "tjohoo"
    # yield min(map(judge_directions, lid_directionss()), key=operator.itemgetter(2))
