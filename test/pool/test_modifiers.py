import unittest
from src.pool.modifiers import *
import src

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
    self.assertIn({"value": 80}, go({"value": 10}))
