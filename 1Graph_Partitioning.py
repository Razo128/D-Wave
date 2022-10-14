# Graph Partitioning by Ryan McKay (https://github.com/Razo128)
#   Code based on: https://cloud.dwavesys.com/leap/example-details/222052595/ (https://github.com/dwave-examples/graph-partitioning)
#             and: https://cloud.dwavesys.com/leap/example-details/222054079/ (https://github.com/dwave-examples/maximum-cut)
#---------------------------
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

# Set tunable parameters
num_reads = 1000
gamma = 80

# Create and design graph
G = nx.gnp_random_graph(40, 0.2)

print("Graph on {} nodes created with {} out of {} possible edges.".format(len(G.nodes), len(G.edges), len(G.nodes) * (len(G.nodes)-1) / 2))

# Initialize Q matrix
Q = defaultdict(int)

# Fill in Q matrix, using QUBO
# Objective
for u, v in G.edges:
    Q[(u,u)] += 1
    Q[(v,v)] += 1
    Q[(u,v)] += -2

# Constraint
for u in G.nodes:
    Q[(u,u)] += gamma*(1-len(G.nodes))

for u, v in combinations(G.nodes, 2):
    Q[(u,v)] += 2*gamma

# Set chain strength
chain_strength = gamma*len(G.nodes)

# Run the QUBO on the solver
sampler = EmbeddingComposite(DWaveSampler())
response = sampler.sample_qubo(Q,
                               chain_strength=chain_strength,
                               num_reads=num_reads,
                               label='Graph Partitioning')

# See if the best solution found is feasible, and if so print the number of cut edges.
sample = response.record.sample[0]

# In the case when n is odd, the set may have one more or one fewer nodes
if sum(sample) in [math.floor(len(G.nodes)/2), math.ceil(len(G.nodes)/2)]:
    num_cut_edges = 0
    for u, v in G.edges:
        num_cut_edges += sample[u] + sample[v] - 2*sample[u]*sample[v]
    print("Valid partition found with", num_cut_edges, "cut edges.")
else:
    print("Invalid partition.")

# Display results to user
# Grab best result
lut = response.first.sample

# Interpret and process best result in terms of nodes and edges
S0 = [node for node in G.nodes if not lut[node]]
S1 = [node for node in G.nodes if lut[node]]
cut_edges = [(u, v) for u, v in G.edges if lut[u]!=lut[v]]
uncut_edges = [(u, v) for u, v in G.edges if lut[u]==lut[v]]

print("Set 0: ", str(S0))
print("Set 1: ", str(S1))

# Display best result
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, nodelist=S0, node_color='r')
nx.draw_networkx_nodes(G, pos, nodelist=S1, node_color='c')
nx.draw_networkx_edges(G, pos, edgelist=cut_edges, style='dashdot', alpha=0.5, width=3)
nx.draw_networkx_edges(G, pos, edgelist=uncut_edges, style='solid', width=3)
nx.draw_networkx_labels(G, pos)

filename = "Graph_Partition_plot.png"
plt.savefig(filename, bbox_inches='tight')
print("\nYour plot is saved to {}".format(filename))

dwave.inspector.show(response)
