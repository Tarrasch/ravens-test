class Selector:
  def __init__(self, selects, punishment, message):
    self.selects = selects
    self.punishment = punishment
    self.message = message

  def __repr__(self):
    return self.message

def infer_selectors(figure):
  return [Selector(lambda subfig: True, 0, "All")]
