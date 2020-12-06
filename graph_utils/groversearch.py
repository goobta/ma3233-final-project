from qiskit import BasicAer
from qiskit.tools.visualization import plot_histogram
from qiskit.aqua import QuantumInstance
from qiskit.aqua.algorithms import Grover
from qiskit.aqua.components.oracles import TruthTableOracle

from typing import List
from time import time

from evaluators import HamiltonianEvaluator
import graph_types as t
# from . import graph_types as t


def get_truth_map(truth_table) -> str:
    """Take in a dictionary truth mapping and convert it to the readable bitmap

    :param truth_table: The tuple:bool dictionary
    :return: A string of the equivalent truth_table
    """
    # Oracle takes a string representation of the binary truth table like '1100001'
    binary_repr = ''
    for key in truth_table:
        binary_repr += str(int(truth_table[key]))  # Abuse of casting to send True -> 1 -> '1'

    # Length of bitmap needs to be a power of 2
    # This bitwise operation checks to see that the value of length is in fact a power of 2
    # https://stackoverflow.com/questions/57025836/how-to-check-if-a-given-number-is-a-power-of-two
    # Add '0' to the END, the bitmap is considered ordered with the MSB as the 0th bit.
    while not (len(binary_repr) != 0 and len(binary_repr) & (len(binary_repr) - 1) == 0):
        binary_repr += '0'

    return binary_repr


def run_grovers(graph_edge_set: List[t.edge], plot: bool = False) -> List[t.edge]:
    """Run Grover's Algorithm on the given graph edge set

    :param graph_edge_set:
        The set of edges for the graph. Comes in a list of Tuple[u, v] form.
            Tuple[u,v] is an edge in E where u and v are vertices in V.
    :param plot:
        True if you want it plotted by the visualizer.
    :return:
        A subset of the graph_edge_set that is a Hamilton cycle, or None if one does not exist.
            Returns the subset in the same form as the edge set input.
    """
    evaluator = HamiltonianEvaluator(graph_edge_set)
    truth_table = evaluator.generate_truth_table()
    truth_map = get_truth_map(truth_table)

    start = time()
    oracle = TruthTableOracle(truth_map)
    grover = Grover(oracle)  # Wow that's nice that this already exists
    result = grover.run(QuantumInstance(BasicAer.get_backend('qasm_simulator'), shots=1024))
    end = time()
    print('Grover\'s search on n = {} vertices:\nTime elapsed: {}s'.format(len(evaluator.vertices), end - start))

    if plot:
        plot_histogram(result['measurement'])
        #result['circuit'].draw(ouput='mpl', filename='grover_circuit{}.png'.format(truth_map))
        # can't draw the circuit for some reason which is a bit frustrating

    # result[top_measurement] gives the binary number of the index of the map
    # This is a terrifying amount of casts
    index = int(result['top_measurement'], 2)
    result = list(truth_table.items())
    result = list(result[index][0])
    return result
