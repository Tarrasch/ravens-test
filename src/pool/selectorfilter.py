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
    return len(f(fig1)) > 0 and f(fig1) == f(fig2)

  def filter_fig(self, fig):
    return filter(self.subfig_selector, fig)


def selectorfilter_pool(figure_pairs):
  return infer_selectorfilters(sum(sum(figure_pairs, []), []))
  # return concat_map(selectorfilter_pool_, figure_pairs)

def selectorfilter_pool_(figure_pair):
  print "..."
  # return infer_selectorfilters(figure_pair[0])

# def helper():
#   print "..."

# def infer_from_subfig(keys, ):
#   print "..."

# def infer_from_guess(keys, ):


def infer_selectorfilters(fig):
  for sz in range(2, 5):
    punishment = 10000#*max(10**(5-sz), 1)
    # for subfig in fig:
    #   for keys in combinations(subfig, sz):
    #     def mk_selector(keys, subfig):
    #       def check(other):
    #         return all(other.get(k) == subfig[k] for k in keys)
    #       return check
    #     mini_subfig = dict((k, v) for k, v in subfig.iteritems() if k in keys)
        # yield SelectorFilter(mk_selector(keys, subfig),
        #                    punishment,
        #                    "Should be like %s" % mini_subfig)

    
    all_keys = frozenset(concat_map(lambda x: x.keys(), fig))
    print(all_keys)
    get_values = lambda key: frozenset(map(lambda sub: sub.get(key,
      "NotNone"), fig))
    keyvalues = concat_map(lambda k: [[k, v] for v in get_values(k)], all_keys)
    pprint(keyvalues)
    for keys in combinations(all_keys, sz):
      print(keys)
      for values in product(*map(get_values, keys)):
        print(values)
        def mk_selector(keys, values):
          def check(subfig):
            l = [subfig.get(k) == v for k, v in zip(keys, values) if k in
                subfig]
            return len(l) > 0 and all(l)
          return check
        yield SelectorFilter(mk_selector(keys, values),
                             punishment,
                             "Look at properties %s" % zip(keys, values))



# def infer_selectorfilters(fig):

