import numpy as np
from operator import itemgetter
import pylab as pl
from pprint import pprint

def s(fig): pl.imshow(fig); pl.gray(); pl.show()

def annotate_rotations(props):
  return map(annotate_rotation, props)

def annotate_rotation(p_subfig):
  r_id = p_subfig['shape_id']
  represent = p_subfig['props'][r_id]['Image']
  self = p_subfig['Image']

  # [for q in range(4):
  def rxor(q):
    a = lambda fun, n: reduce(lambda f1, f2: lambda x: f1(f2(x)), [fun]*n, lambda x: x)
    cand = a(np.rot90, q)(self)
    rx, ry = represent.shape
    cx, cy = cand.shape
    mx = max(rx, cx)
    my = max(ry, cy)
    ms = (mx, my)
    ri = np.zeros(ms)
    ci = np.zeros(ms)
    ri[:rx,:ry]= represent
    ci[:cx,:cy]= cand
    ri = ri > 0.5
    ci = ci > 0.5
    return (ri^ci).sum()*(1+q/10.0) # Favor low rotation

  return {'rot': min(range(4), key = rxor)*90 }
    # s(ri)
    # s(ci)
    # pprint(ri)
    # pprint(ci)
    # s(ri ^ ci)
    # s(np.zeros((5,5)))
