import numpy as np
from operator import itemgetter
import pylab as pl
from pprint import pprint

def s(fig): pl.imshow(fig); pl.gray(); pl.show()

def annotate_rotations(props):
  return map(annotate_rotation, props)

def annotate_rotation(p_subfig):
  r_id = p_subfig['shape_id']
  represent = p_subfig['props'][r_id]['FilledImageFit']
  self = p_subfig['FilledImageFit']

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
    xor = ri^ci
    ratio = 1.0*xor.sum()/(ci.sum()+ri.sum())
    return (xor.sum()*(1+q/10.0), ratio, q) # Favor low rotation

  data = map(rxor, range(4))
  val, _ratio, q = min(data, key=itemgetter(0))
  _val, ratio, _q = max(data, key=itemgetter(1))
  ok = ratio > 0.2
  return {'rot': (q*ok)*90 }
