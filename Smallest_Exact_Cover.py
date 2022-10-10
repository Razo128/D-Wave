# Graph Problems by Ryan McKay (https://github.com/Razo128)

# Import necessary packages
import math
import networkx as nx
from collections import defaultdict
from itertools import combinations
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
import dwave.inspector
# Set up matplot lib for displaying solution graph
import matplotlib
matplotlib.use("agg")
from matplotlib import pyplot as plt
# Import random for generating V subsets
import random

# Set tunable parameters
num_reads = 1000
gamma = 10

# Create array U of elements (integers)
num_elements = 20
U = list(range(0, num_elements))

# Create subsets V
num_subsets = 10
V = []
for i in range(0, num_subsets):
    V.append(sorted(random.sample(range(0, num_elements), random.randint(1, num_elements)))) # some V subsets may be the same

# Create and design graph
G = nx.Graph()
G.add_nodes_from(range(0, num_subsets))
for i in range(0, num_subsets):
    for j in range(i+1, num_subsets):
        if len(list(set(V[i]).intersection(set(V[j])))) > 0:
               G.add_edge(i, j)

# Initialize Q matrix
Q = defaultdict(int)

# Fill in Q matrix, using QUBO
# Objective
for u in G.nodes:
    Q[(u,u)] += 1

# Constraint
for u, v in combinations(G.nodes, 2):
	  Q[u, v] += gamma # non-disjoint pairs of subsets in R
     # subsets not in R not connected to any subsets in R
    

# Set chain strength
chain_strength = 

# Run the QUBO on the solver
sampler = EmbeddingComposite(DWaveSampler())
response = sampler.sample_qubo(Q,
                               chain_strength=chain_strength,
                               num_reads=num_reads,
                               label='Example - Graph Problem')

# See if the best solution found is feasible, and if so print the number of cut edges.
sample = response.record.sample[0]

# Processing, if necessary


# Display results to user
# Grab best result
lut = response.first.sample

# Interpret best result in terms of nodes and edges
S0 = [node for node in G.nodes if not lut[node]]
S1 = [node for node in G.nodes if lut[node]] # Edit where necessary

print("Set 0: ", str(S0))
print("Set 1: ", str(S1)) # Edit where necessary

# Display best result
pos = nx.spring_layout(G)
nx.draw_networkx_nodes()
nx.draw_networkx_edges()

filename = "Graph_Problem_plot.png"
plt.savefig(filename, bbox_inches='tight')
print("\nYour plot is saved to {}".format(filename))

dwave.inspector.show(response)
