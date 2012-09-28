import unittest
from src.directions import *

class TestDirectionFunctions(unittest.TestCase):
  def test_all(self):
    got = map(lambda x: map(direction_mnemonic, x), lid_directionss())
    exp = [["down", "right"], ["down", "diag"], ["right", "diag"]]
    self.assertEqual(got, exp)

