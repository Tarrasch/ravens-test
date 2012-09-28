import unittest
from src.filter import *
import src

class TestSolveFunctions(unittest.TestCase):
  def test_select_best_filter(self):
    filters = [Filter(lambda a, b: a > b, 5, "old-should-be-bigger"),
               Filter(lambda a, b: True, 10, "accept everything"),
               Filter(lambda a, b: a < b, 6, "new should be bigger")]
    got = select_best_filter(filters, 100, 200).punishment
    exp = 6
    self.assertEqual(got, exp)

    got = select_best_filter(filters, 200, 100).punishment
    exp = 5
    self.assertEqual(got, exp)
