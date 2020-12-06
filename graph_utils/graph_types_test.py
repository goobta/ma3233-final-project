from parameterized import parameterized
import unittest

from . import evaluators as ge
from groversearch import run_grovers


class TestHamiltonianEvaluator(unittest.TestCase):
    def test_vertex_evaluation(self):
        edges = [(1, 2), (3, 4), (4, 1), (4, 6), (5, 7)]
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
        truth = [(('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'A')),
                 (('A', 'B'), ('C', 'D'), ('A', 'C'), ('B', 'D')),
                 (('B', 'C'), ('D', 'A'), ('A', 'C'), ('B', 'D'))]

        evlr = ge.HamiltonianEvaluator(edge_set)
        truth_table = evlr.generate_truth_table()

        for edges, is_hamiltonian in truth_table.items():
            if edges in truth:
                self.assertTrue(is_hamiltonian)
            else:
                self.assertFalse(is_hamiltonian)


class TestGroverSearch(unittest.TestCase):
    def test_grover(self):
        graph_str = '''
    A---------------B
    |-\          -- |
    |  -\      -/   |
    |    --\--/     |
    |    --/--\     |
    |  -/      -\   |
    |-/          -- |
    D-------------- C'''
        edge_set = [('A', 'B'), ('B', 'C'), ('C', 'D'),
                    ('D', 'A'), ('A', 'C'), ('B', 'D')]
        valid_cycles = [[('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'A')],
                        [('A', 'B'), ('C', 'D'), ('A', 'C'), ('B', 'D')],
                        [('B', 'C'), ('D', 'A'), ('A', 'C'), ('B', 'D')]]
        result = run_grovers(edge_set, True, graph_str)
        self.assertTrue(result in valid_cycles)

    def test_larger_graph(self):
        graph_str = '''
        A-----------D
       /|           |\\
      / |           | \\
     /  |           |  \\
    C   |           |   E
     \  |           |  /
      \ |           | /
       \|           |/
        B-----------F
        '''
        edge_set = [('A', 'B'), ('A', 'D'), ('A', 'C'), ('D', 'E'),
                    ('D', 'F'), ('C', 'B'), ('E', 'F'), ('B', 'F')]
        valid_cycle = [('A', 'D'), ('A', 'C'), ('D', 'E'), ('C', 'B'), ('E', 'F'), ('B', 'F')]
        result = run_grovers(edge_set, True, graph_str)
        self.assertTrue(result == valid_cycle)

    def test_disconnected_graph(self):
        graph_str = '''
        A           D
       /|           |\\
      / |           | \\
     /  |           |  \\
    C   |           |   E
     \  |           |  /
      \ |           | /
       \|           |/
        B           F'''
        edge_set = [('A', 'B'), ('A', 'C'), ('D', 'E'),
                    ('D', 'F'), ('C', 'B'), ('E', 'F')]
        self.assertTrue(run_grovers(edge_set, True, graph_str) == [])

    def test_disconnected_graph_with_extra_edge(self):
        graph_str = '''
        A           D
       /|           |\\
      / |           | \\
     /  |           |  \\
    C   |           |   E
     \  |           |  /
      \ |           | /
       \|           |/
        B-----------F'''
        edge_set = [('A', 'B'), ('A', 'C'), ('D', 'E'),
                    ('D', 'F'), ('C', 'B'), ('E', 'F'), ('B', 'F')]
        self.assertTrue(run_grovers(edge_set, True, graph_str) == [])


if __name__ == '__main__':
    unittest.main()
