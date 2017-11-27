#!/usr/bin/python

import argparse
import matplotlib.pyplot as plt
import networkx as nx
import numpy
import os.path

# Command line parameters
parser = argparse.ArgumentParser(description='Basic analysis for a graph given in CSV format')
parser.add_argument('--summary', dest='summary', action='store_true', default=False)
parser.add_argument('--centrality', dest='centrality', action='store_true', default=False)
parser.add_argument('--degreedist', dest='degreedist', action='store_true', default=False)
parser.add_argument('--verbose', dest='verbose', action='store_true', default=False)
parser.add_argument('--nnodes', dest='nnodes', action='store', default=10, type=int)
parser.add_argument('filename', nargs=1)
args = parser.parse_args()

# argument to the script is a path to an adjacency list
g = nx.read_adjlist(args.filename[0], create_using=nx.DiGraph())
g_undirected = nx.read_adjlist(args.filename[0])

if args.summary:
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

if args.centrality:
    # print most central users in reverse order
    centrality = [(k, v) for k, v in nx.out_degree_centrality(g).items()]
    centrality.sort(key=lambda t: t[1], reverse=True)
    if args.verbose:
        print('Most central users by in-degree centrality')
    for uid, _ in centrality[:args.nnodes]:
        print(uid)

    # NB: betweenness centrality takes exponential time to compute
    # centrality = [(k, v) for k, v in nx.betweenness_centrality(g).items()]
    # centrality.sort(key=lambda t: t[1], reverse=True)
    # print('Most central users by betweenness centrality', [uid for uid, _ in centrality[:10]])

if args.degreedist:
    # plotting degree distributions
    plt.title('In-Degree Histogram for ' + args.filename[0])
    plt.xlabel('In-Degree')
    plt.ylabel('N')
    plt.axis([0, 500, 0, 250]) # defining a ymax that makes it possible to see long tail
    plt.hist(in_degree, bins=range(max(in_degree)+1))
    plt.savefig(os.path.splitext(args.filename[0])[0] + '_indegree_hist.png')
    plt.close()

    plt.title('Out-Degree Histogram for ' + args.filename[0])
    plt.xlabel('Out-Degree')
    plt.ylabel('N')
    plt.axis([0, 500, 0, 250]) # defining a ymax that makes it possible to see long tail
    plt.hist(out_degree, bins=range(max(out_degree)+1))
    plt.savefig(os.path.splitext(args.filename[0])[0] + '_outdegree_hist.png')


### some interesting things to work with in the future; many are exponential runtime
# Average node connectivity
# print('Average Node Connectivity:', nx.average_node_connectivity(g))

# See https://networkx.github.io/documentation/latest/reference/algorithms/index.html for more ideas
