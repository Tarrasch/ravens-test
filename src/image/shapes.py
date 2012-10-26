from operator import itemgetter

def add_shape(props):
  for prop in props:
    prop['shape'] = 'best_shape'
  # t = 1.0
  # def are_alike(a, b):
  #   return True
  # for prop in props:

  #   yield shape

def annotate_shapes(props):
  return map(lambda p: { 'shape': p['shape'] }, props)
