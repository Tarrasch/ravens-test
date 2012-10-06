import unittest
from src.pool.selectors import *
from itertools import *
from pprint import pprint
import src

def split_on_condition(seq, condition):
  # http://stackoverflow.com/a/949490/621449
  a, b = [], []
  for item in seq:
      (a if condition(item) else b).append(item)
  return a,b

def get_validator_generic(fig):
  selectors = list(infer_selectors(fig))
  def make_validator(fig_in):
    def validator(exists, noexists):
      return any(map(lambda sfselects:
        all(map(lambda subfig: sfselects(subfig), exists))
        and
        all(map(lambda subfig: not sfselects(subfig), noexists))
        , map(lambda s: s.mk_subfig_selector(fig_in), selectors)))
    return validator
  return make_validator

def get_validator(fig):
  return get_validator_generic(fig)(fig)

class TestSelectorFunctions(unittest.TestCase):

  def test_infer_selectors(self):
    fig = [{}]
    v = get_validator(fig)

    # It should always yield one ALL selector
    self.assertTrue(v([{}], []))
    self.assertTrue(v([{"irrelevant":"property"}], []))

    # test min/max
    fig = [{"x": x, "y": y} for x, y in product(range(3),
      repeat=2)]
    gv = get_validator_generic(fig)
    v = gv(fig)
    self.assertEqual(len(fig), 9) # sanity check
    self.assertTrue (v(*split_on_condition(fig, lambda sf: sf["x"]==2)))
    self.assertFalse(v(*split_on_condition(fig, lambda sf: sf["x"]==1)))
    self.assertTrue (v(*split_on_condition(fig, lambda sf: sf["x"]==0)))

    self.assertTrue (v(*split_on_condition(fig, lambda sf: sf["y"]==2)))
    self.assertFalse(v(*split_on_condition(fig, lambda sf: sf["y"]==1)))
    self.assertTrue (v(*split_on_condition(fig, lambda sf: sf["y"]==0)))

    self.assertFalse(v([{"x":2}, {"y":2}], [{"x":1}]))
    self.assertTrue (v([{"x":2}, {"x":2}], []))
    self.assertFalse(v([{"x":2}, {"x":1}], [[{"y":1}]]))

    # test dynamix min/max
    fig_in = [{"x": x, "y": y} for x, y in product(range(3), range(2))]
    # Now only 2 rows
    v = gv(fig_in)
    self.assertTrue (v(*split_on_condition(fig_in, lambda sf: sf["x"]==2)))
    self.assertFalse(v(*split_on_condition(fig_in, lambda sf: sf["x"]==1)))
    self.assertTrue (v(*split_on_condition(fig_in, lambda sf: sf["x"]==0)))

    # Note! Now y=1 is max, this is "only interesting" case!
    self.assertTrue (v(*split_on_condition(fig_in, lambda sf: sf["y"]==1)))
    self.assertTrue (v(*split_on_condition(fig_in, lambda sf: sf["y"]==0)))

    # A selector for having a property to a specific value
    fig = [{"a": "a", "b": "b", "c": "c"}]
    tbt = map(lambda kv: dict([(kv[0], kv[1])]), (product("abc", repeat=2)))
    v = get_validator(fig)
    key_is_value = lambda d: d.keys() == d.values()
    self.assertTrue (v(*split_on_condition(tbt[0:3], key_is_value)))
    self.assertTrue (v(*split_on_condition(tbt[3:6], key_is_value)))
    self.assertTrue (v(*split_on_condition(tbt[6:9], key_is_value)))
    self.assertTrue (v(*split_on_condition(tbt[5:9], key_is_value)))
