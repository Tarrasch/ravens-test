import unittest
from src.pool.modifiers import *
import src

def get_all_modifier(*figs):
  modifiers = infer_modifiers(figs)
  return lambda subfig: map(lambda mod: mod.modify(subfig), modifiers)

class TestSelectorFunctions(unittest.TestCase):

  def test_infer_selectors(self):
    fig_A = [{}]
    fig_B = [{}]
    go = get_all_modifier(fig_A, fig_B)

    self.assertIn({}, go({}))
