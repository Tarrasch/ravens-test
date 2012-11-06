import os.path
import cv2

def parse(dir):
  """
  Given directory where representation images are, return an representation
  with the images. This can then either be used directly (visual reasoning) or
  be converted to a tree with the images replaced with a property based
  reasoning.
  """
  grid = map(lambda xs: map(lambda x: path_to_fig(x), xs), grid_paths(dir))
  alts = map(lambda x: path_to_fig(x), alternative_paths(dir))
  d = dict([('grid', grid)] + [(i, alts[i-1]) for i in range(1,len(alts)+1)])
  return d

def alternative_paths(dir):
  for a in range(1,100):
    file_path = "%s/%s.png" % (dir, a)
    if os.path.exists(file_path):
      yield file_path

def grid_paths(dir):
  fp = lambda y,x: "%s/grid/%s-%s.png" % (dir, y, x)
  n = 2 + os.path.exists(fp(3,2))
  array = [["def"]*n]*(n-1) + [["def"]*(n-1)]
  return [[fp(y+1,x+1) for x in range(n) if y < n-1 or x < n-1] for y in range(n)]

def path_to_fig(path):
  return segment(cv2.imread(path, cv2.CV_LOAD_IMAGE_GRAYSCALE))

def segment(img):
  # return pymorph.close((255-img) > 128, Bc = pymorph.sebox(r=1))
  return (255-img) > 128
