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

class Transformer(Filter):
  def __init__(self, transform, punishment, message):
    self.transform = transform
    self.punishment = punishment
    self.message = message

  def composite(self, other_transformer):
    transform = lambda fig: other_transformer.transform(self.transform(fig))
    punishment = self.punishment + other_transformer.punishment
    message = self.message + " -- and then " + other_transformer.message
    return Transformer(transform, punishment, message)

  def accept(self, fig1, fig2):
    return normalize(self.transform(fig1)) == normalize(fig2)

  def __repr__(self):
    return self.message

def normalize(dicts):
  return sorted(map(lambda dic: sorted(dic.iteritems()), dicts))

def create_filter(selector, modification, copy):
  def transform(fig):
    sfselects = selector.mk_subfig_selector(fig)
    def apply(subfig):
      if sfselects(subfig):
        yield modification.modify(subfig)
        if copy:
          yield subfig
      else:
        yield subfig
    return list(concat_map(apply, fig))

  punishment = selector.punishment + modification.punishment
  message = "for (%s) %s (%s)" % (selector.message,
                                  "copy with" if copy else "modify",
                                  modification.message)
  return Transformer(transform, punishment, message)


def transformation_pool(figure_pairs):
  return set(concat_map(transformation_pool_, figure_pairs))

def transformation_pool_(figure_pair):
  cf = lambda triple: create_filter(*triple)
  transform_ingredients = product(infer_selectors(figure_pair[0]),
      infer_modifiers(figure_pair),
      [False, True])
  return imap(cf, transform_ingredients) # TODO: add composition later
