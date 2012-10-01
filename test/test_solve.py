import unittest
from src.solve import *
import src

class TestSolveFunctions(unittest.TestCase):
  def test_get_filterss(self):
    src.solve.fetch_pools = lambda g, d: g+"o"+d
    src.solve.std_directions = lambda: ["a", "b"]
    got = src.solve.get_filterss("k")
    exp = {"a": list("koa"), "b": list("kob")}
    self.assertEqual(got, exp)

  def test_get_from_figure(self):
    grid = [["a", "b"],
            ["c"]]
    self.assertEqual(get_from_figure(grid, (1, 1)), "a")
    self.assertEqual(get_from_figure(grid, (0, 1)), "c")
