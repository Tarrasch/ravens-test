import unittest
from src.pool.transforms import *
from src.pool.helpers import *
from src.pool.selectors import *
from src.pool.modifiers import *


class TestTransformerFunctions(unittest.TestCase):

  def test_accept(self):
    ch = lambda x: {"key":x}
    tr = Transformer(lambda l: map(lambda dic: ch(dic["key"]/2), l), 0, "copy-all")
    fig = map(ch, [6,7,8])
    self.assertFalse(tr.accept(fig, map(ch, [3, 4])))
    self.assertTrue(tr.accept(fig, map(ch, [3, 4, 3])))

  def test_create_filter(self):
    import src
    src.pool.transforms.normalize = lambda x: x
    selector = Selector(lambda sf: sf == "b", 3, "")
    modifier = Modifier(lambda sf: sf + "c", 5, "")
    filt1 = create_filter(selector, modifier, False)
    self.assertEqual(filt1.punishment, 8)
    fig = ["a", "b"]
    self.assertFalse(filt1.accept(fig, []))
    self.assertTrue(filt1.accept(fig, ["a", "bc"]))
    filt1 = create_filter(selector, modifier, True)
    self.assertTrue(filt1.accept(fig, ["a", "bc", "b"]))
