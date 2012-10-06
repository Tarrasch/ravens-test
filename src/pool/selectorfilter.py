from src.filter import *
from src.pool.helpers import *
from pprint import pprint

class SelectorFilter(Filter):
  def __init__(self, subfig_selector, punishment, message):
    self.subfig_selector = subfig_selector
    self.punishment = punishment
    self.message = message

  def accept(self, fig1, fig2):
    f = lambda x: self.filter_fig(x)
    nf = lambda x: normalize(f(x))
    return nf(fig1) == nf(fig2)

  def filter_fig(self, fig):
    return filter(self.subfig_selector, fig)


def selectorfilter_pool(figure_pairs):
  return infer_selectorfilters(sum(sum(figure_pairs, []), []))

def infer_selectorfilters(fig):
  for sz in range(1, 6):
    punishment = 1000*max(10**(5-sz), 1)
    all_keys = frozenset(concat_map(lambda x: x.keys(), fig))
    get_values = lambda key: frozenset(map(lambda sub: sub.get(key,
      "NotNone"), fig))
    get_values = lambda key: frozenset(sub[key] for sub in fig if key in sub)
    all_keyvalues = concat_map(lambda k: [[k, v] for v in get_values(k)], all_keys)
    for keyvalues in combinations(all_keyvalues, sz):
      def mk_selector(keyvalues):
        def check(subfig):
          l = [subfig.get(k) == v for k, v in keyvalues]
          return any(l)
        return check
      yield SelectorFilter(mk_selector(keyvalues),
                           punishment,
                           "No changes in " + str(keyvalues))

