from top import fig_to_props, massage_props, prop_to_rep
from operator import itemgetter
from pprint import pprint

def create_rep(image_tree):
  pprint(image_tree)
  grid = image_tree['grid']
  alts = [image_tree[k] for k in range(100) if image_tree.has_key(k)]
  grid = map(lambda xs: map(lambda x: fig_to_props(x), xs), grid)
  alts = map(lambda x: fig_to_props(x), alts)
  props = sum(sum(grid, []) + alts, [])
  massage_props(props) # Like add shape annotations etc
  grid = map(lambda xs: map(lambda x: prop_to_rep(x), xs), grid)
  alts = map(lambda x: prop_to_rep(x), alts)
  dicts = sum(sum(grid, []) + alts, [])
  clean_properties(dicts)
  d = dict([('grid', grid)] + [(i, alts[i-1]) for i in range(1,len(alts)+1)])
  return d

def clean_properties(dicts):
  # Just for efficiency and easier debugging
  for k in dicts[0].keys():
    if len(set(map(itemgetter(k), dicts))) <= 1:
      for d in dicts:
        del d[k]
