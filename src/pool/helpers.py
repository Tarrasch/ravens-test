from itertools import *

def concat_map(function, items):
  return chain(*map(function, items)) # this will work more likely