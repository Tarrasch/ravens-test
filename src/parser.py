from image.top import fig_to_props, massage_props, prop_to_rep, segment
import os.path
import cv2
from operator import itemgetter

def parse(dir):
  """
  Given directory where representation images are
  """
  # path_to_rep(alternative_paths(dir).next())
  # path_to_rep(grid_paths(dir)[0][0])
  # return {}
  grid = map(lambda xs: map(lambda x: path_to_props(x), xs), grid_paths(dir))
  alts = map(lambda x: path_to_props(x), alternative_paths(dir))
  props = sum(sum(grid, []) + alts, [])
  massage_props(props) # Like add shape annotations etc
  grid = map(lambda xs: map(lambda x: prop_to_rep(x), xs), grid)
  alts = map(lambda x: prop_to_rep(x), alts)
  dicts = sum(sum(grid, []) + alts, [])
  clean_properties(dicts)
  d = dict([('grid', grid)] + [(str(i), alts[i-1]) for i in range(1,len(alts)+1)])
  return d

def clean_properties(dicts):
  # Just for efficiency and easier debugging
  for k in dicts[0].keys():
    if len(set(map(itemgetter(k), dicts))) <= 1:
      for d in dicts:
        del d[k]

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


def path_to_props(path):
  return fig_to_props(path_to_fig(path))

