
# Let a transformation be a tuple:
#
# (f, desc)
#
# where desc is a string description and f(grid, alt) is a real value judgement
# of how well the transformation applies. 1.0 = perfect, 0 = not at all
#

def transformations():
  return [
  ]

def t2d(modifier):
  def fun(grid, alt):
    return "uni"
  return fun

