import unittest
from src.pool.selectors import *
import src

def get_any(fig):
  selectors = infer_selectors(fig)
  def find(subfig):
    return any(map(lambda sel: sel.selects(subfig), selectors))
def get_anys(fig):
  selectors = list(infer_selectors(fig))
  def find(subfigs):
    return any(map(lambda sel: all(map(lambda subfig:
      sel.selects(subfig), selectors)), subfigs))
  return find

def get_any(fig):
  find = get_anys(fig)
  return lambda subfig: find([subfig])

class TestSelectorFunctions(unittest.TestCase):

  def test_infer_selectors(self):
    fig = [{}]
    my_any = get_any(fig)

    # It should always yield one ALL selector
    self.assertTrue(my_any({}))
    self.assertTrue(my_any({"irrelevant":"property"}))
