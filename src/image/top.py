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
from prop import region_prop
from position import annotate_positions
from shapes import annotate_shapes, add_shape


def s(img): pl.imshow(img); pl.gray(); pl.show()

def massage_props(props):
  # Oblivious of which subfigure belongs where!
  add_shape(props)
  return props

def fig_to_props(img):
  fig = segment(img)
  # s(fig)
  subfigures = get_subfigures(fig)
  rp = lambda subfig: region_prop(fig, subfig)
  props = map(rp, subfigures)
  return props

def prop_to_rep(props):
  # Oblivious of how others figures look like!
  a_positions = annotate_positions(props)
  a_shapes = annotate_shapes(props)
  annotations = [a_positions, a_shapes]
  return merge_annotations(annotations)

def merge_annotations(annotations):
  # f_annotations = filter(lambda x: len(list(groupby((x)))) > 1, annotations)
  f_annotations = annotations
  def go(*anns):
    return dict([(k, v) for k, v in sum(map(lambda d: list(d.iteritems()), anns), [])])
  # return map(go, *f_annotations) if len(f_annotations) > 0 else [{}]*len(annotations[0])
  return map(go, *f_annotations)



def segment(img):
  # return pymorph.close((255-img) > 128, Bc = pymorph.sebox(r=1))
  return (255-img) > 128

def get_subfigures(fig):
  cs,_= cv2.findContours( fig.astype('uint8'), mode=cv2.RETR_EXTERNAL,
                               method=cv2.CHAIN_APPROX_SIMPLE )
  return cs
