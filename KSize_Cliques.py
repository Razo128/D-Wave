# KSize_Cliques by Ryan McKay (https://github.com/Razo128)

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

# Choose K
K = 10

# Set tunable parameters
num_reads = 1000
gamma = K+10

# Create and design graph
G = nx.gnp_random_graph(40, 0.85)

# Initialize Q matrix
Q = defaultdict(int)

# Fill in Q matrix, using QUBO
# Objective
for u, v in G.edges:
    Q[(u,v)] += -1

# Constraint
for u in G.nodes:
    Q[(u,u)] += gamma*(1 - 2*K)

for u, v in combinations(G.nodes, 2):
    Q[(u,v)] += gamma*2

# Set chain strength
chain_strength = 2*gamma*K

# Run the QUBO on the solver
sampler = EmbeddingComposite(DWaveSampler())
response = sampler.sample_qubo(Q,
                               chain_strength=chain_strength,
                               num_reads=num_reads,
                               label='Example - Graph Problem')

# See if the best solution found is feasible.
sample = response.record.sample[0]

# Display results to user
# Grab best result
lut = response.first.sample

# Interpret best result in terms of nodes and edges
S0 = [node for node in G.nodes if not lut[node]]
S1 = [node for node in G.nodes if lut[node]] # Edit where necessary
clique_edges = [(u, v) for u, v in G.edges if lut[u]==lut[v]]
other_edges = [(u, v) for u, v in G.edges if lut[u]!=lut[v]]
missed_edges = []
present_edges = []
for u, v in combinations(S1, 2):
	if (u, v) not in clique_edges:
		missed_edges.append((u,v))
	else:
		present_edges.append((u,v))

print("A candidate clique of size ", len(S1), "/", K, "was found with ", len(missed_edges), " missing edges.")
print("Clique set: ", S1)
print("Missing edges: ", missed_edges)

# Display best result
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, nodelist=S1, node_color='r')
nx.draw_networkx_edges(G, pos, edgelist=present_edges, style='solid', width=3)
nx.draw_networkx_labels(G, pos, labellist=S1)

filename = "KSize_Clique_plot.png"
plt.savefig(filename, bbox_inches='tight')
print("\nYour plot is saved to {}".format(filename))

dwave.inspector.show(response)
