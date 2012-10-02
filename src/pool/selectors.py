from src.pool.helpers import concat_map

class Selector:
  def __init__(self, selects, punishment, message):
    self.selects = selects
    self.punishment = punishment
    self.message = message

  def __repr__(self):
    return self.message

def infer_selectors(fig):
  yield Selector(lambda subfig: True, 0, "All")
  all_keys = frozenset(concat_map(lambda x: x.keys(), fig))
  for key in all_keys:
    # Max/min capability
    values = map(lambda x: x.get(key), fig)
    if "__cmp__" in dir(values[0]): # Number like
      for fold, desc in [(min, "min"), (max, "max")]:
        selector = lambda subfig, v=fold(values), key=key: subfig.get(key) == v
        yield Selector(
              selector,
              10,
              "%s by %s" % (desc, key))

