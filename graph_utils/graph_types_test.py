import unittest

from . import evaluators as ge


class TestHamiltonianEvaluator(unittest.TestCase):
  def test_vertex_evaluation(self):
    edges = [(1, 2), (3, 4), (4, 1), (4, 6), (5,7)]
    evlr = ge.HamiltonianEvaluator(edges)
    self.assertSetEqual(evlr.vertices, {1, 2, 3, 4, 5, 6, 7})


if __name__ == '__main__':
  unittest.main()