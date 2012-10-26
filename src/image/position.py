from operator import itemgetter

def annotate_positions(props):
  bboxes = map(itemgetter('BoundingBox'), props)
  ul_most = min(bboxes, key = lambda x: sum(x[0:2]))
  ap = lambda p_subfig: annotate_position(ul_most, p_subfig)
  return map(ap, props)

def annotate_position(ul_most, p_subfig):
  origo_x, origo_y, dx, dy = ul_most
  x, y, _1, _2 = p_subfig['BoundingBox']
  ir = lambda x: int(round(x))
  return { 'x': ir((x-origo_x)/dx),
           'y': ir((y-origo_y)/dy) }

