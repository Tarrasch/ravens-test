from operator import itemgetter
from pprint import pprint
import pylab as pl
def s(fig): pl.imshow(fig); pl.gray(); pl.show()

def add_shape(props):
  # pprint(map(itemgetter('Extent'), props))
  # pprint(zip(map(itemgetter('NumPixels'), props),
  #   map(itemgetter('FilledArea'), props)))
  # pprint(map(itemgetter('Fillity'), props))
  # pprint(map(itemgetter('EquivDiameter'), props))
  # pprint(map(itemgetter('Eccentricity'), props))
  # pprint(map(itemgetter('Orientation'), props))
  # props = sorted(props) # Make deterministic!
  t = 1.0
  def are_alike(a, b):
    # Ok the proper solution would be some sort of k means clustering with a
    # very smart way to determine k
    d = lambda feat: abs(a[feat]-b[feat])
    ma = lambda feat: max(a[feat], b[feat])
    ratio = lambda feat: d(feat)/ma(feat)
    return sum(
     [d('Extent')*4,
      d('Eccentricity')/2,
      ratio('MajorAxisLength'),
      ratio('MinorAxisLength'),
      d('CentLength')/ma('MajorAxisLength')*5,
      ]) < 0.8

  candidate_shapes = []
  for i in range(len(props)):
    # Is it like any other known shape ?
    for sh_id in candidate_shapes + [i]:
      if(are_alike(props[sh_id], props[i])):
        props[i]['shape'] = "shape_" + str(sh_id)
        props[i]['shape_id'] = sh_id
        if sh_id == i:
          candidate_shapes += [i]
        break
      else:
        a = props[sh_id]
        # b = props[i]
        # d = lambda feat: abs(a[feat]-b[feat])
        # ma = lambda feat: max(a[feat], b[feat])
        # ratio = lambda feat: d(feat)/ma(feat)
        # pprint( (
        #  [d('Extent')*2,
        #   d('Eccentricity')/2,
        #   ratio('MajorAxisLength'),
        #   ratio('MinorAxisLength'),
        #   d('CentLength')/ma('MajorAxisLength')*5,
        #   ]))
        # s(a['Image'])
        # s(b['Image'])
    assert('shape' in props[i])


def annotate_shapes(props):
  return map(lambda p: { 'shape': p['shape'] }, props)
