from typing import List, Set
from . import graph_types as t

class HamiltonianEvaluator:
  def __init__(self, edges: List[t.edge]):
    """Create a new HamiltonianEvaluator.

    Args:
        edges (List[t.edge]): The edge set
    """
    self.edges: List[t.edge] = edges
    self.vertices: Set[t.vertex] = {v for e in self.edges for v in e}