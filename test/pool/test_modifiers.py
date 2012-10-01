import unittest
from src.pool.modifiers import *
import src
from pprint import pprint

def get_all_modifier(*figs):
  modifiers = list(infer_modifiers(figs))
  return lambda subfig: map(lambda mod: mod.modify(subfig), modifiers)

class TestSelectorFunctions(unittest.TestCase):

  def test_infer_modifiers(self):
    # "Type-checking"
    fig_A = [{}]
    fig_B = [{}]
    go = get_all_modifier(fig_A, fig_B)
    self.assertIn({}, go({}))

    # Check simple transforming capability
    fig_A = [{"value": "white"}]
    fig_B = [{"value": "black"}]
    go = get_all_modifier(fig_A, fig_B)
    self.assertIn({"value": "black"}, go({"value": "white"}))
    self.assertIn({"value": "black"}, go({"value": "white"}))
    self.assertIn({"value": "black"}, go({"value": "orange"}))

    # Check subtractive capability
    fig_A = [{"value": 70}]
    fig_B = [{"value": 80}]
    go = get_all_modifier(fig_A, fig_B)
    self.assertIn({"value": 30}, go({"value": 20}))
    self.assertNotIn({"value": 31}, go({"value": 20}))
    self.assertIn({"value": 60}, go({"value": 50}))
    self.assertIn({"value": 80, "other": 45},
                  go({"value": 10, "other": 45}))
    # Also for the example fig:
    sec_0   = {'angle': 90, 'shape': 'sector', 'start': 0}
    sec_90  = {'angle': 90, 'shape': 'sector', 'start': 90}
    sec_m90 = {'angle': 90, 'shape': 'sector', 'start': -90}
    go = get_all_modifier([sec_0], [sec_m90])
    self.assertIn(sec_0, go(sec_90))
    # And again but for right direction
    go = get_all_modifier([sec_0], [sec_90])
    self.assertIn(sec_0, go(sec_m90))

