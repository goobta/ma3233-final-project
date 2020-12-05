from parameterized import parameterized
import unittest

from . import evaluators as ge


class TestHamiltonianEvaluator(unittest.TestCase):
  def test_vertex_evaluation(self):
    edges = [(1, 2), (3, 4), (4, 1), (4, 6), (5,7)]
    evlr = ge.HamiltonianEvaluator(edges)
    self.assertSetEqual(evlr.vertices, {1, 2, 3, 4, 5, 6, 7})

  @parameterized.expand([
    ('not_enough_edges', [('A', 'B')], False),
    ('not_enough_vertices', [('A', 'B'), ('B', 'C'),
                             ('C', 'A'), ('A', 'B')], False),
    ('no_cycle', [('A', 'B'), ('B', 'C'),
                    ('B', 'C'), ('C', 'D')], False),
    ('correct', [('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'A')], True)
  ])
  def test_hamiltonian(self, name, edges, is_hamiltonian):
    """
            Test Graph
         A---------------B
         |-\          -- |
         |  -\      -/   |
         |    --\--/     |
         |    --/--\     |
         |  -/      -\   |
         |-/          -- |
         D-------------- C
    """
    edge_set = [('A', 'B'), ('B', 'C'), ('C', 'D'), 
                ('D', 'A'), ('A', 'C'), ('B', 'D')]

    evlr = ge.HamiltonianEvaluator(edge_set)
    self.assertEqual(evlr.is_hamiltonian(edges), is_hamiltonian)

  def test_truth_table(self):
    """
            Test Graph
         A---------------B
         |-\          -- |
         |  -\      -/   |
         |    --\--/     |
         |    --/--\     |
         |  -/      -\   |
         |-/          -- |
         D-------------- C
    """
    edge_set = [('A', 'B'), ('B', 'C'), ('C', 'D'), 
                ('D', 'A'), ('A', 'C'), ('B', 'D')]
    truth = (('A', 'B'), ('B', 'C'), ('C', 'D'), ('A', 'D'))

    evlr = ge.HamiltonianEvaluator(edge_set)
    truth_table = evlr.generate_truth_table()

    for edges, is_hamiltonian in truth_table.items():
      if edges == truth_table:
        self.assertTrue(is_hamiltonian)
      else:
        self.assertFalse(is_hamiltonian)


if __name__ == '__main__':
  unittest.main()