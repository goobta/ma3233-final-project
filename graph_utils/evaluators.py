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

  def is_hamiltonian(self, edges: List[t.edge]) -> bool:
    # Edge Count constraint
    if len(edges) != len(self.vertices):
      return False

    # Vertex Saturation constraint
    included_vertices = {v for e in edges for v in e}
    if included_vertices != self.vertices:
      return False

    # Connectedness & cycle constraint
    # Create a dictionary from vertex -> (active_degree, "leader")
    vertex_meta = {v: [0, v] for v in included_vertices}
    for e_from, e_to in edges:
      leader = min(vertex_meta[e_from][1], vertex_meta[e_to][1])

      vertex_meta[e_from][1] = leader
      vertex_meta[e_from][0] += 1
      vertex_meta[e_to][1] = leader
      vertex_meta[e_to][0] += 1
      
    first_leader = next(iter(vertex_meta.values()))[1]
    for degree, leader in vertex_meta.values():
      if degree != 2 or leader != first_leader:
        return False
    return True