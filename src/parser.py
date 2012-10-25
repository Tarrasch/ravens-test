from image.top import img_to_rep
import os.path
import cv2

def parse(dir):
  """
  Given directory where representation images are
  """
  grid = map(lambda xs: map(lambda x: path_to_rep(x), xs), grid_paths(dir))
  alts = map(lambda x: path_to_rep(x), alternative_paths(dir))
  d = dict([('grid', grid)] + [(str(i), alts[i-1]) for i in range(1,len(alts)+1)])
  return d

def alternative_paths(dir):
  for a in range(1,100):
    file_path = "%s/%s.png" % (dir, a)
    if os.path.exists(file_path):
      yield file_path

def grid_paths(dir):
  fp = lambda y,x: "%s/grid/%s-%s.png" % (dir, y, x)
  n = 2 + os.path.exists(fp(3,2))
  print n
  array = [["def"]*n]*(n-1) + [["def"]*(n-1)]
  print array
  for y in range(1,4):
    for x in range(1,4):
      file_path = fp(y, x)
      if os.path.exists(file_path):
        array[y-1][x-1] = file_path
  return array

def path_to_img(path):
  return cv2.imread(path, cv2.CV_LOAD_IMAGE_GRAYSCALE)


def path_to_rep(path):
  return img_to_rep(path_to_img(path))

