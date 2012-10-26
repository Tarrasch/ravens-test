from operator import itemgetter
from pprint import pprint

def add_shape(props):
  pprint(map(itemgetter('Extent'), props))
  # props = sorted(props) # Make deterministic!
  t = 1.0
  def are_alike(a, b):
    # Ok the proper solution would be some sort of k means clustering with a
    # very smart way to determine k
    return abs(a['Extent'] - b['Extent']) < 0.15

  candidate_shapes = []
  for i in range(len(props)):
    # Is it like any other known shape ?
    for sh_id in candidate_shapes + [i]:
      if(are_alike(props[sh_id], props[i])):
        props[i]['shape'] = "shape_" + str(sh_id)
        if sh_id == i:
          candidate_shapes += [i]
        break
    assert('shape' in props[i])


def annotate_shapes(props):
  return map(lambda p: { 'shape': p['shape'] }, props)
