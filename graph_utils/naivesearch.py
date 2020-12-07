from typing import List, Tuple
from time import time
from itertools import combinations

#import graph_types as t
#import evaluators as ge
from . import graph_types as t
from . import evaluators as ge


def search(edge_set: List[t.edge]) -> List[t.edge]:
    """Naive search through all the possible combinations given by the truth table

    :param edge_set: The list of edges that make up a graph
    :return: The list of the edges that form a Hamilton cycle if one exists. [] otherwise.
    """
    result = []
    start = time()
    graph = ge.HamiltonianEvaluator(edge_set)
    comb = combinations(graph.edges, len(graph.vertices))
    for sub_graph in comb:
        if graph.is_hamiltonian(sub_graph):
            result = sub_graph
            break
    end = time()
    print('Ran basic search')
    print('Time elapsed: {}s'.format(end - start))
    print('Found edge set: {}'.format(result))
    return result
