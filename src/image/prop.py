import cv2
from itertools import *
import numpy as np
import pylab as pl
from pprint import pprint
import pymorph
import math
def s(img): pl.imshow(img); pl.gray(); pl.show()


def region_prop(fig, subfig):
  # Inspired by:
  # http://stackoverflow.com/a/9059648/621449
  c = subfig

# set up the 'FilledImage' bit of regionprops.
  FilledImage = np.zeros(fig.shape[0:2]).astype('uint8')
# set up the 'ConvexImage' bit of regionprops.
  ConvexImage = np.zeros(fig.shape[0:2]).astype('uint8')
# calculate some things useful later:
  m = cv2.moments(c)

# ** regionprops **
  Area          = m['m00']
  Perimeter     = cv2.arcLength(c,True)
# bounding box: x,y,width,height
  BoundingBox   = cv2.boundingRect(c)
# centroid    = m10/m00, m01/m00 (x,y)
  Centroid      = ( m['m10']/m['m00'],m['m01']/m['m00'] )

# EquivDiameter: diameter of circle with same area as region
  EquivDiameter = np.sqrt(4*Area/np.pi)
# Extent: ratio of area of region to area of bounding box
  Extent        = Area/(BoundingBox[2]*BoundingBox[3])

# FilledImage: draw the region on in white
  cv2.drawContours( FilledImage, [c], 0, color=255, thickness=-1 )
# calculate indices of that region..
  regionMask    = (FilledImage==255)
# FilledArea: number of pixels filled in FilledImage
  FilledArea    = np.sum(regionMask)
# PixelIdxList : indices of region.
# (np.array of xvals, np.array of yvals)
  PixelIdxList  = regionMask.nonzero()

# CONVEX HULL stuff
# convex hull vertices
  ConvexHull    = cv2.convexHull(c)
  ConvexArea    = cv2.contourArea(ConvexHull)
# Solidity := Area/ConvexArea
  Solidity      = Area/ConvexArea
# convexImage -- draw on ConvexImage
  cv2.drawContours( ConvexImage, [ConvexHull], -1,
                    color=255, thickness=-1 )

# ELLIPSE - determine best-fitting ellipse.
  centre,axes,angle = cv2.fitEllipse(c)
  MAJ = np.argmax(axes) # this is MAJor axis, 1 or 0
  MIN = 1-MAJ # 0 or 1, minor axis
# Note: axes length is 2*radius in that dimension
  MajorAxisLength = axes[MAJ]
  MinorAxisLength = axes[MIN]
  Eccentricity    = np.sqrt(1-(axes[MIN]/axes[MAJ])**2)
  Orientation     = angle
  EllipseCentre   = centre # x,y

  Test = FilledImage.astype('uint8')
  mf = cv2.moments(Test)
  CentroidFilled = ( mf['m10']/mf['m00'],mf['m01']/mf['m00'] )

# # ** if an image is supplied with the fig:
# # Max/Min Intensity (only meaningful for a one-channel img..)
#   MaxIntensity  = np.max(img[regionMask])
#   MinIntensity  = np.min(img[regionMask])
# # Mean Intensity
#   MeanIntensity = np.mean(img[regionMask],axis=0)
# # pixel value
#   PixelValues   = img[regionMask]
  x0, y0, dx, dy = BoundingBox
  x1, y1 = x0 + dx, y0 + dy
  Image = fig[y0:y1, x0:x1]
  OImage = fig[y0-1:y1+1, x0-1:x1+1]
  NumPixels  = Image.sum()
  Fillity = (NumPixels+0.0)/FilledArea
  crx, cry = (CentroidFilled[0]-x0, CentroidFilled[1]-y0)
  dxc = crx-(x1-x0)/2.0
  dyc = cry-(y1-y0)/2.0
  CentLength = math.sqrt(dxc*dxc + dyc*dyc)
  # print(Centroid)
  # print(CentroidFilled)
  # print(((x1-x0)/2.0, (y1-y0)/2))
  # print(CentLength)
  # print("---")
  # s(Image)
  # s(FilledImage)

  Thin = pymorph.thin(OImage)
  # s(Thin)
  # s(Thin)
  if num_holes(Image) >= 2:
    Inner = removeOuter(Thin)
    # s(Inner)
  # Thick = pymorph.thick(Image)
  # s(Thick)


  # e = lambda fig: pymorph.erode(fig)
  # d = lambda fig: pymorph.dilate(fig)
  # o = lambda fig: pymorph.open(fig)
  # c = lambda fig: pymorph.close(fig)
  # a = lambda fun, n: reduce(lambda f1, f2: lambda x: f1(f2(x)), [fun]*n, lambda x: x)
  # s((a(e, 3))(Image))

  ret = dict((k,v) for k, v in locals().iteritems() if k[0].isupper())
  return ret

def removeOuter(fig):
  q = [[0,0]]
  dy = [1, 0, -1, 0, 1, -1,  1, -1]
  dx = [0, 1, 0, -1, 1, -1, -1,  1]
  res = np.zeros(fig.shape)
  vis = set()
  res[:,:] = fig[:,:]
  while q:
    y0, x0 = q.pop()
    res[y0][x0] = False
    if (y0, x0) in vis:
      continue
    vis.add((y0, x0))
    for y, x in [(y0+dy[i],x0+dx[i]) for i in range(8)]:
      if x < 0 or y < 0 or y >= fig.shape[0] or x >= fig.shape[1]:
        continue
      if fig[y0][x0] == False:
        q.append((y,x))
  return res

def num_holes(fig):
  return len(cv2.findContours( fig.astype('uint8'), mode=cv2.RETR_TREE,
                               method=cv2.CHAIN_APPROX_NONE )[1][0])-1
