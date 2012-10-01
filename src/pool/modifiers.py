from copy import copy
from src.pool.helpers import concat_map

class Modifier:
  def __init__(self, modify, punishment, message):
    self.modify = modify
    self.punishment = punishment
    self.message = message

def infer_modifiers(figure_pair):
  fig_A, fig_B = figure_pair
  yield Modifier(lambda x: x, 10, "no modification")
  all_keys = frozenset(concat_map(lambda x: x.keys(), fig_A+fig_B))
  for key in all_keys:
    # Becoming capability
    for subfig_B in fig_B:
      value_B = subfig_B.get(key)
      modifier = map_fig(lambda _: value_B, key)
      yield Modifier(modifier, 10, "set `%s`s to %s" % (key, value_B))

      # Additive capability
      for subfig_A in fig_A:
        value_A = subfig_A.get(key)
        if type(value_A) == type(value_B) and "__sub__" in dir(value_A):
          delta = (value_B-value_A)
          modifier = map_fig(lambda v: v + delta, key)
          yield Modifier(modifier, 10, "inc `%s`s by %s" % (key, delta))


def map_fig(modifier, key):
  def mod_subfig(subfig):
    subfig = copy(subfig)
    subfig.update([(key, modifier(subfig.get(key)))])
    return subfig
  return mod_subfig
