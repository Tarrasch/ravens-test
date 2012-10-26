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
from operator import itemgetter
from prop import region_prop


def s(img): pl.imshow(img); pl.gray(); pl.show()

def fig_to_rep(img):
  img = segment(img)
  fig = img
  # s(fig)
  subfigures = get_subfigures(fig)
  rp = lambda subfig: region_prop(fig, subfig)
  props = map(rp, subfigures)
  a_positions = annotate_positions(props)
  return a_positions

def segment(img):
  # return pymorph.close((255-img) > 128, Bc = pymorph.sebox(r=1))
  return (255-img) > 128

def get_subfigures(fig):
  cs,_= cv2.findContours( fig.astype('uint8'), mode=cv2.RETR_EXTERNAL,
                               method=cv2.CHAIN_APPROX_SIMPLE )
  return cs

def annotate_positions(props):
  bboxes = map(itemgetter('BoundingBox'), props)
  ul_most = min(bboxes, key = lambda x: sum(x[0:2]))
  ap = lambda p_subfig: annotate_position(ul_most, p_subfig)
  return map(ap, props)

def annotate_position(ul_most, p_subfig):
  origo_x, origo_y, dx, dy = ul_most
  x, y, _1, _2 = p_subfig['BoundingBox']
  ir = lambda x: int(round(x))
  return { 'x': ir((x-origo_x)/dx),
           'y': ir((y-origo_y)/dy) }
