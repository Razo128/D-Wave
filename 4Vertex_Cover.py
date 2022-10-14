# Vertex Cover by Ryan McKay (https://github.com/Razo128)

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
gamma = 10

# Create and design graph
G = nx.gnp_random_graph(40, 0.1)

# Initialize Q matrix
Q = defaultdict(int)

# Fill in Q matrix, using QUBO
# Objective
for u in G.nodes:
    Q[(u,u)] += 1

# Constraint
for u, v in G.edges:
    Q[(u,v)] += gamma
    Q[(u,u)] += -gamma
    Q[(v,v)] += -gamma

# Set chain strength
chain_strength = 400

# Run the QUBO on the solver
sampler = EmbeddingComposite(DWaveSampler())
response = sampler.sample_qubo(Q,
                               chain_strength=chain_strength,
                               num_reads=num_reads,
                               label='Vertex Cover')

# Obtain the best run
sample = response.record.sample[0]

# Processing, if necessary


# Display results to user
# Grab best result
lut = response.first.sample

# Interpret and process best result in terms of nodes and edges
S0 = [node for node in G.nodes if not lut[node]]
S1 = [node for node in G.nodes if lut[node]]

print("Included vertices: ", len(S1), ": ", str(S1)) 

# Display best result
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, nodelist=S0, node_color='w')
nx.draw_networkx_nodes(G, pos, nodelist=S1, node_color='b')
nx.draw_networkx_edges(G, pos, edgelist=G.edges, style='solid', width=3)
nx.draw_networkx_labels(G, pos)

filename = "Vertex_Cover_plot.png"
plt.savefig(filename, bbox_inches='tight')
print("\nYour plot is saved to {}".format(filename))

dwave.inspector.show(response)
