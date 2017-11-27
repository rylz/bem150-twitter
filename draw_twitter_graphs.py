#!/usr/bin/python

import argparse
import json
import matplotlib.pyplot as plt
import networkx as nx
import random

import twitter_metadata

COLORS = 'rgbk'

parser = argparse.ArgumentParser(description='Draw visualizations of a graph given in CSV format')
parser.add_argument('--clusters', action='store', type=str)
parser.add_argument('--sample', action='store', type=float, default=1.0)
parser.add_argument('filename', nargs=1)
args = parser.parse_args()

g = nx.read_adjlist(args.filename[0], create_using=nx.DiGraph())

if args.clusters:
    with open(args.clusters, 'r') as cluster_file:
        clusters = json.loads(cluster_file.read())

    # sample the clusters to make the visualization more usable
    if args.sample < 1.0:
        for i, cluster in clusters.items():
            clusters[i] = set(random.sample(cluster, int(len(cluster)*args.sample)))

    # draw the subgraph of these clusters
    cluster_union = set.union(*clusters.values())
    cluster_union.update(set([influencer for influencer in clusters.keys()]))
    cgraph = g.subgraph(cluster_union)
    # position the influencers statically so that they're spaced apart
    influencer_positions = nx.circular_layout(cgraph.subgraph(clusters.keys()))
    pos = nx.spring_layout(cgraph, pos=influencer_positions, fixed=clusters.keys())
    influencer_labels = {str(k): v for k, v in twitter_metadata.get_user_names(clusters.keys()).items()}
    for i, influencer in enumerate(clusters.keys()):
        nx.draw_networkx_nodes(
                cgraph, pos, nodelist=list(clusters[influencer]),
                node_color=COLORS[i % len(COLORS)], node_size=15, alpha=0.5)
        nx.draw_networkx_nodes(
                cgraph, pos, nodelist=[influencer],
                node_color=COLORS[i % len(COLORS)], node_size=50)
        nx.draw_networkx_labels(
                cgraph, pos, labels=influencer_labels, font_size=8, font_color='w')
    nx.draw_networkx_edges(cgraph, pos, width=1.0, alpha=0.05)
    plt.show()
