import unittest
from src.pool.transforms import *
from src.pool.helpers import *
from src.pool.selectors import *
from src.pool.modifiers import *


class TestTransformerFunctions(unittest.TestCase):

  def test_create_filter(self):
    selector = Selector(lambda sf: sf == "b", 3, "")
    modifier = Modifier(lambda sf: sf + "c", 5, "")
    filt1 = create_filter(selector, modifier, False)
    self.assertEqual(filt1.punishment, 8)
    fig = ["a", "b"]
    self.assertFalse(filt1.accept(fig, []))
    self.assertTrue(filt1.accept(fig, ["a", "bc"]))
    filt1 = create_filter(selector, modifier, True)
    self.assertTrue(filt1.accept(fig, ["a", "bc", "b"]))
