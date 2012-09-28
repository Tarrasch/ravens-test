import unittest
from src.pool.pool import *

def unroll(item):
  if "__iter__" in dir(item):
    return map(unroll, item)
  else:
    return item

class TestPoolFunctions(unittest.TestCase):

  def test_positions(self):
    got = list(positions(2, [1, 0]))
    exp = [((0, 0), (1, 0))]
    self.assertEqual(got, exp)

    got = list(positions(2, [0, 1]))
    exp = [((0, 0), (0, 1))]
    self.assertEqual(got, exp)

    got = list(positions(2, [1, 1]))
    exp = [((1, 0), (0, 1))]
    self.assertEqual(got, exp)

    got = list(positions(3, [0, 1]))
    exp = [
            ((0, 0), (0, 1)),
            ((0, 1), (0, 2)),
            ((1, 0), (1, 1)),
            ((1, 1), (1, 2)),
            ((2, 0), (2, 1)),
          ]
    self.assertEqual(got, exp)

  def test_lid_positions(self):
    got = unroll(lid_positions(2))
    down =  [[[0, 0], [1, 0]]]
    right = [[[0, 0], [0, 1]]]
    diag =  [[[1, 0], [0, 1]]]
    exp = [[down, right], [down, diag], [right, diag]]
    self.assertEqual(got, exp)

    got = unroll(lid_positions(3))
    self.assertEqual(len(got), 3)
    self.assertEqual(len(got[0]), 2)
    self.assertEqual(len(got[0][0]), 5)
    self.assertEqual(len(got[0][0][0]), 2)
    self.assertEqual(len(got[0][0][0][0]), 2)

  def test_fetch_pools(self):
    import src.pool.pool
    def mocked_create_pool(figure_pairs):
      if figure_pairs == "test":
        return ["got", "here"]
      figure_pairs = list(figure_pairs)
      figure_pair = figure_pairs[0]
      f1, f2 = figure_pair
      return "%s-%s" % (f1[0]["fig"], f2[0]["fig"])

    src.pool.pool.create_pool = mocked_create_pool
    self.assertEqual(src.pool.pool.create_pool("test"), ["got", "here"])
    fig = "fig"
    grid = [[[{fig: "11"}], [{fig: "12"}]], [[{fig: "21"}]]]
    got = unroll(src.pool.pool.fetch_pools(grid))
    exp = [["11-21", "11-12"], ["11-21", "21-12"], ["11-12", "21-12"]]
    self.assertEqual(got, exp)
