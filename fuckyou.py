import cv2
import numpy
import numpy as np
import scipy
import pylab as pl
import pylab
import pymorph
from scipy import misc

def s(fig): pl.imshow(fig); pl.gray(); pl.show()

e = lambda fig: pymorph.erode(fig)
d = lambda fig: pymorph.dilate(fig)
o = lambda fig: pymorph.open(fig)
c = lambda fig: pymorph.close(fig)
a = lambda fun, n: reduce(lambda f1, f2: lambda x: f1(f2(x)), [fun]*n, lambda x: x)

img= 255-cv2.imread('reps/2/2.png', cv2.CV_LOAD_IMAGE_GRAYSCALE)
imgb = img > 128
BW=imgb

# grab contours
cs,_ = cv2.findContours( BW.astype('uint8'), mode=cv2.RETR_LIST,
                             method=cv2.CHAIN_APPROX_SIMPLE )
# set up the 'FilledImage' bit of regionprops.
filledI = np.zeros(BW.shape[0:2]).astype('uint8')
# set up the 'ConvexImage' bit of regionprops.
convexI = np.zeros(BW.shape[0:2]).astype('uint8')

# for each contour c in cs:
# will demonstrate with cs[0] but you could use a loop.
print "There are %i number of regions" % len(cs)
for i in range(len(cs)):
  c = cs[i]

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
  cv2.drawContours( filledI, cs, i, color=255, thickness=-1 )
# calculate indices of that region..
  regionMask    = (filledI==255)
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
# convexImage -- draw on convexI
  cv2.drawContours( convexI, [ConvexHull], -1,
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

# ** if an image is supplied with the BW:
# Max/Min Intensity (only meaningful for a one-channel img..)
  MaxIntensity  = np.max(img[regionMask])
  MinIntensity  = np.min(img[regionMask])
# Mean Intensity
  MeanIntensity = np.mean(img[regionMask],axis=0)
# pixel values
  PixelValues   = img[regionMask]
  x0, y0, dx, dy = BoundingBox
  x1, y1 = x0 + dx, y0 + dx
  Image = BW[y0:y1, x0:x1]

  print "Orientation = %s" % Orientation
  print "BoundingBox = " + str(BoundingBox)

  s(Image)
# s(convexI)
# s(filledI)
