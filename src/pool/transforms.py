# This is filters that given pictures A and B, returns a validator
# like this
#
# t(A) == B
#
# The transformation function t is infered (or guessed) from the inputs.

from src.filter import *
from src.pool.helpers import *
from src.pool.selectors import infer_selectors
from src.pool.modifiers import infer_modifiers
from src.work_print import work_print

class Transformer(Filter):
  def __init__(self, transform, punishment, message):
    self.transform = transform
    self.punishment = punishment
    self.message = message

  def compose(self, other_transformer):
    transform = lambda fig: other_transformer.transform(self.transform(fig))
    punishment = self.punishment + other_transformer.punishment
    message = self.message + " -- and then " + other_transformer.message
    return Transformer(transform, punishment, message)

  def accept(self, fig1, fig2):
    return normalize(self.transform(fig1)) == normalize(fig2)

  @staticmethod
  def identity_transformer():
    t = Transformer(lambda fig: fig, 0, "Identity-transformer")
    t.compose = lambda other: other
    return t

  def __repr__(self):
    return self.message

def normalize(dicts):
  return sorted(map(lambda dic: sorted(dic.iteritems()), dicts))

def create_filter(selector, modification, action):
  def transform(fig):
    sfselects = selector.mk_subfig_selector(fig)
    def apply(subfig):
      if action != "remove":
        if sfselects(subfig):
          yield modification.modify(subfig)
          if action == "copy":
            yield subfig
        else:
          yield subfig
    return list(concat_map(apply, fig))

  punishment = selector.punishment + modification.punishment
  message = "for (%s) %s (%s)" % (selector.message,
                                  action,
                                  modification.message)
  return Transformer(transform, punishment, message)


def transformation_pool(figure_pairs):
  return productify(set(concat_map(transformation_pool_,
    figure_pairs)), 3)

def productify(transformers, r):
  uncomposeds = concat_map(lambda i: product(transformers, repeat=i), range(r))
  def compose_transformers(ts):
    work_print()
    return reduce(lambda t1, t2: t1.compose(t2), ts, Transformer.identity_transformer())
  return map(compose_transformers, uncomposeds)

def transformation_pool_(figure_pair):
  cf = lambda triple: create_filter(*triple)
  transform_ingredients = product(infer_selectors(figure_pair[0]),
      infer_modifiers(figure_pair),
      ["inplace", "copy", "remove"])
  return imap(cf, transform_ingredients)
