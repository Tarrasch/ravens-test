from itertools import *

def concat_map(function, items):
  return list(chain(*map(function, items)))

def normalize(dicts):
  return sorted(map(lambda dic: sorted(dic.iteritems()), dicts))
