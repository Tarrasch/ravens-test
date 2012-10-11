from itertools import chain
from src.pool.helpers import concat_map

class Selector:
  def __init__(self, mk_subfig_selector, punishment, message):
    self.mk_subfig_selector = mk_subfig_selector
    self.punishment = punishment
    self.message = message

  def __repr__(self):
    return self.message

def simpleSelector(subfig_selector, punishment, message):
  return Selector(lambda _fig: subfig_selector, punishment, message)

def infer_selectors(fig):
  yield simpleSelector(lambda subfig: True, 0, "All")
  all_keys = frozenset(concat_map(lambda x: x.keys(), fig))
  for key in all_keys:
    values = frozenset(map(lambda x: x.get(key), fig))
    # Max/min capability
    if "__cmp__" in dir(iter(values).next()): # Number like
      minn = lambda xs: min(chain([99999], xs))
      maxx = lambda xs: max(chain([-99999], xs))
      for fold, desc in [(minn, "min"), (maxx, "max")]:
        def give_mk_subfig_selector(fig_in, fold=fold, key=key):
          values_in = map(lambda x: x.get(key), fig_in)
          v = fold(values_in)
          selector = lambda subfig: subfig.get(key) == v
          return selector
        yield Selector(
              give_mk_subfig_selector,
              30,
              "%s by %s" % (desc, key))
    # Key is as one of known keys
    else:
      for value in values:
        selector = lambda subfig, value=value, key=key: subfig.get(key) == value
        yield simpleSelector(
              selector,
              30,
              "key `%s` is `%s`" % (key, value))

