import cv2
import numpy
import numpy as np
import scipy
import pylab as pl
import pylab
import pymorph
from scipy import misc

def s(fig): pl.imshow(fig); pl.gray(); pl.show()

def img_to_rep(img):
  img = segment(img)
  # s(img)

def segment(img):
  return pymorph.close((255-img) > 128, Bc = pymorph.sebox(r=1))


