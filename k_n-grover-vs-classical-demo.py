# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.7.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # Grover's on $K_n$
#
# Create a complete graph, delete some of the edges, and juxtapose the computations.

# ## Imports

# Import our custom framework first

from graph_utils import groversearch, naivesearch, evaluators

# Misc imports

# +
from qiskit.tools.visualization import plot_histogram
from time import time

import matplotlib.pyplot as plt
import networkx as nx
import itertools
import random
import math
import scipy

# %matplotlib inline
# -

# ## Graph Creation

# Set $n$ = $v$ = The number of vertices

n = int(input('Enter the value for n (# of vertices): '))

# Generate a complete graph...

edge_set = list(itertools.combinations(range(n), 2))

# ...and visualize it

# +
graph = nx.Graph()
graph.add_edges_from(edge_set)

fig = plt.figure()
ax = plt.axes()

nx.draw_networkx(graph, ax=ax)
# -

# ### (Optional) Delete a subset of the edges to make the problem harder

del_perc = float(input('Percentage of edges to delete: ')) / 100

# Delete the edges...

# +
for _ in range(int(del_perc * len(edge_set))):
    random_edge = random.choice(edge_set)
    edge_set.remove(random_edge)
    
len(edge_set)
# -

# ...and revisualize it

# +
graph = nx.Graph()
graph.add_edges_from(edge_set)

fig = plt.figure()
ax = plt.axes()

nx.draw_networkx(graph, ax=ax)
# -

# ## Report Constants

print("""
Vertices: {}
Edges: {}
Total Combinations: {}""".format(n, len(edge_set), 
                               math.comb(len(edge_set), n)))

# ## Compare the two solutions

# ### Naive search

evlr = evaluators.HamiltonianEvaluator(edge_set)

# Recall that the naive search is simply going through all of the edge subsets and running the Hamiltonian cycle test.

# +
start = time()
truth_table = evlr.generate_truth_table()
end = time()

print('It took {:.8f}s for the naive search'.format(end - start))
# -

# Find out how many hamiltonian cycles there are and print them out

# +
combinations = []
ham_cycles = []
for i, (comb, is_ham) in enumerate(truth_table.items()):
    combinations.append(comb)
    
    if is_ham:
        ham_cycles.append(i)
        
print('There are {} total hamiltonian cycles: \n'.format(len(ham_cycles)))
for i in ham_cycles:
    print(combinations[i])
# -

# ### Grover's Search

# Compute the min number of shots

shots = math.ceil(math.sqrt(len(combinations)))
shots #= 1024

# Data preprocessing for qiskit

truth_map = groversearch.get_truth_map(truth_table)

# Run Grovers

result = groversearch.call_grover(truth_map, len(evlr.vertices),
                                  shots=shots)

# Visualize the results

plot_histogram(result['measurement'], title='Possible Hamiltonian Cycles\n for $K_{}$'.format(n))

# ## Binary2EdgeSet

bin2edgeset = lambda bin_combo: combinations[int(str(bin_combo), 2)]
binary = input('Enter the binary representation: ')
print(bin2edgeset(binary))
print('Is hamiltonian?: {}'.format(truth_table[bin2edgeset(binary)]))


