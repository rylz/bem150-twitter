__doc__ = """

Library for custom graph analysis algorithm implementations.

Meant to be a one-stop shop for things not provided by networkx, including:
    * Neighbor Cumulative Degree Centrality (NCC)

"""

def ncc_centrality(g, in_degree=True):
    """Compute Neighbor Cumulative Degree Centrality for a graph.

    Find degree centrality of nodes as a sum of degree of their neighbors.

    in_degree param allows caller to switch implementation between in_degree and out_degree centrality measures.

    Based on https://www.cambridge.org/core/journals/political-analysis/article/longitudinal-network-centrality-using-incomplete-data/D2D59F17EB02D8F4B996EB65B05899F0

    """
    result = {n: 0 for n in g.nodes()}
    for n in g.nodes():
        if in_degree:
            neighbors = g.predecessors(n)
            degree = g.out_degree(n)
        else:
            neighbors = g.successors(n)
            degree = g.in_degree(n)

        for p in neighbors:
            result[p] += degree

    return list(result.items())
