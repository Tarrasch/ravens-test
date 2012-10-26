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
from rotation import annotate_rotations


def s(img): pl.imshow(img); pl.gray(); pl.show()

def massage_props(props):
  # Oblivious of which subfigure belongs where!
  add_shape(props)
  for p in props:
    p['props'] = props # A neccesarry back door
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
  annotators = [
    annotate_positions,
    annotate_shapes,
    annotate_rotations,
    annotate_filled,
    ]
  return merge_annotators(props, annotators)

def merge_annotators(props, annotators):
  all_props = props[0]['props']
  hash_dict = lambda d: tuple(sorted(d.iteritems()))
  f_annotators = filter(lambda f: len(set(map(hash_dict, f(all_props)))) > 1, annotators)
  # for f in annotators: print (set(map(hash_dict, f(all_props))))
  def go(*anns):
    return dict([(k, v) for k, v in sum(map(lambda d: list(d.iteritems()), anns), [])])
  return map(go, *map(lambda f: f(props), f_annotators))

def annotate_filled(props):
  return [{'filled': 'yes' if p['Fillity'] > 0.9 else 'no' } for p in props]

def segment(img):
  # return pymorph.close((255-img) > 128, Bc = pymorph.sebox(r=1))
  return (255-img) > 128

def get_subfigures(fig):
  cs,_= cv2.findContours( fig.astype('uint8'), mode=cv2.RETR_EXTERNAL,
                               method=cv2.CHAIN_APPROX_NONE )
  return cs
