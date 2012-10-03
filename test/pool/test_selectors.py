import unittest
from src.pool.selectors import *
from itertools import *
import src

def split_on_condition(seq, condition):
  # http://stackoverflow.com/a/949490/621449
  a, b = [], []
  for item in seq:
      (a if condition(item) else b).append(item)
  return a,b

def get_validator(fig):
  selectors = list(infer_selectors(fig))
  def validator(exists, noexists):
    return any(map(lambda sfselects:
      all(map(lambda subfig: sfselects(subfig), exists))
      and
      all(map(lambda subfig: not sfselects(subfig), noexists))
      , map(lambda s: s.mk_subfig_selector(fig), selectors)))
  return validator

class TestSelectorFunctions(unittest.TestCase):

  def test_infer_selectors(self):
    fig = [{}]
    v = get_validator(fig)

    # It should always yield one ALL selector
    self.assertTrue(v([{}], []))
    self.assertTrue(v([{"irrelevant":"property"}], []))

    fig = [{"x": x, "y": y} for x, y in product(range(3),
      repeat=2)]
    v = get_validator(fig)
    self.assertEqual(len(fig), 9) # sanity check
    self.assertTrue (v(*split_on_condition(fig, lambda sf: sf["x"]==2)))
    self.assertFalse(v(*split_on_condition(fig, lambda sf: sf["x"]==1)))
    self.assertTrue (v(*split_on_condition(fig, lambda sf: sf["x"]==0)))

    self.assertTrue (v(*split_on_condition(fig, lambda sf: sf["y"]==2)))
    self.assertFalse(v(*split_on_condition(fig, lambda sf: sf["y"]==1)))
    self.assertFalse(v(*split_on_condition(fig, lambda sf: sf["y"]==1)))

    self.assertFalse(v([{"x":2}, {"y":2}], [{"x":1}]))
    self.assertTrue (v([{"x":2}, {"x":2}], []))
    self.assertFalse(v([{"x":2}, {"x":1}], [[{"y":1}]]))


