from top import fig_to_props, massage_props, prop_to_rep
from operator import itemgetter
from pprint import pprint
from src.tree import *

def create_rep(image_tree):
  prop_tree = map_tree(fig_to_props, image_tree)
  massage_props(collapse_tree(prop_tree)) # Like add shape annotations etc
  rep_tree = map_tree(prop_to_rep, prop_tree)
  clean_properties(collapse_tree(rep_tree))
  return rep_tree

def clean_properties(dicts):
  # Just for efficiency and easier debugging
  for k in dicts[0].keys():
    if len(set(map(itemgetter(k), dicts))) <= 1:
      for d in dicts:
        del d[k]
