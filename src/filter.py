from itertools import ifilter

class Filter:
  def __init__(self, accept, punishment, message = "Unnamed"):
    self.accept = accept
    self.punishment = punishment
    self.message = message

  def __str__(self):
    return self.message

  def __repr__(self):
    return self.message

  def __hash__(self):
    return hash(self.message)

  def __eq__(self, other):
    return self.message == other.message


def select_best_filter(filters, old, new):
  """
  Given a list of filters, the old image and the new image. Return the filter
  from the provided list that satisfies the image transition and has the lowest
  punishment (the best one, simply).
  """
  return min(ifilter(lambda f: f.accept(old, new), filters), key=lambda f: f.punishment)
