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
