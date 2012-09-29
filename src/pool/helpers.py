from itertools import *

def concat_map(creator, figure_pairs):
  return chain(*map(creator, figure_pairs)) # this will work more likely
