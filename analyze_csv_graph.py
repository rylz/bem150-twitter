#!/usr/bin/python

import matplotlib.pyplot as plt
import networkx as nx
import numpy
import os.path
import sys

# argument to the script is a path to an adjacency list
g = nx.read_adjlist(sys.argv[1], create_using=nx.DiGraph())
g_undirected = nx.read_adjlist(sys.argv[1])

### printing a bunch of simple stats
print('Number of nodes:', g.order())
print('Number of edges:', g.size())
connected_components = list(nx.connected_components(g_undirected))
print('Number of connected components (ignoring direction):', len(connected_components))
print('Size of connected components (ignoring direction):',
        sorted([len(component) for component in connected_components], reverse=True)[0:10])
# method returns sets of tuples (node id, degree). we only care about the second item here
in_degree = [degree for id, degree in g.in_degree()]
out_degree = [degree for id, degree in g.out_degree()]
print('Average in-degree:', numpy.average(in_degree))
print('Median in-degree:', numpy.median(in_degree))
print('Average out-degree:', numpy.average(out_degree))
print('Median out-degree:', numpy.median(out_degree))

# plotting degree distributions

plt.title('In-Degree Histogram for ' + sys.argv[1])
plt.xlabel('In-Degree')
plt.ylabel('N')
plt.axis([0, max(in_degree)+1, 0, 250]) # defining a ymax that makes it possible to see long tail
plt.hist(in_degree, bins=range(max(in_degree)+1))
plt.savefig(os.path.splitext(sys.argv[1])[0] + '_indegree_hist.png')

plt.title('Out-Degree Histogram for ' + sys.argv[1])
plt.xlabel('Out-Degree')
plt.ylabel('N')
plt.axis([0, max(out_degree)+1, 0, 250]) # defining a ymax that makes it possible to see long tail
plt.hist(out_degree, bins=range(max(out_degree)+1))
plt.savefig(os.path.splitext(sys.argv[1])[0] + '_outdegree_hist.png')


### some interesting things to work with in the future; many are exponential runtime
# Degree Centrality - returns dictionary of centrality for all nodes 
# could analyze some of the most central nodes
# nx.in_degree_centrality(g))
# nx.out_degree_centrality(g))

# Average node connectivity
# print('Average Node Connectivity:', nx.average_node_connectivity(g))

# See https://networkx.github.io/documentation/latest/reference/algorithms/index.html for more ideas
