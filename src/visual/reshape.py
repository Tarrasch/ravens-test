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
from src.tree import *

def reshape_images(tree):
  imgs = collapse_tree(tree)
  def size(img):
    ys, xs = np.nonzero(img)
    y0, x0, y1, x1 = ys.min(), xs.min(), ys.max()+1, xs.max()+1
    return max(y1-y0, x1-x0)
  max_size = max(map(size, imgs))
  pprint(max_size)

  def resize(img):
    ys, xs = np.nonzero(img)
    y0, x0, y1, x1 = ys.min(), xs.min(), ys.max()+1, xs.max()+1
    new = np.zeros([max_size, max_size])
    new[0:y1-y0,0:x1-x0] = img[y0:y1,x0:x1]
    return new
  return map_tree(resize, tree)
