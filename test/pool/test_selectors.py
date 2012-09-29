import unittest
from src.pool.selectors import *
import src

def get_any(fig):
  selectors = infer_selectors(fig)
  def find(subfig):
    return any(map(lambda sel: sel.selects(subfig), selectors))
  return find

class TestSelectorFunctions(unittest.TestCase):

  def test_infer_selectors(self):
    fig = [{}]
    my_any = get_any(fig)

    # It should always yield one ALL selector
    self.assertTrue(my_any({}))
    self.assertTrue(my_any({"irrelevant":"property"}))
