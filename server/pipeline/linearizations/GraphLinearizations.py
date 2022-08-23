from typing import List

import networkx as nx
import numpy as np
import pandas as pd

from Linearization import *


class GraphLinearization(Linearization):
    """Abstract class for linearizations on graph data, extends the base linearization class to
    account for the different structure of the data."""

    def connect_components(self, G: nx.Graph) -> nx.Graph:
        """Adds simple edges between disconnected components of a given graph, thereby making it
        connected."""
        components = nx.connected_components(G)
        last_node = None

        for component in components:
            if last_node:
                G.add_edge(last_node, list(component)[0])
            last_node = list(component)[0]

        return G

    def remove_cycles(self, G: nx.Graph) -> nx.Graph:
        is_cyclic = True

        while is_cyclic:
            try:
                cycle = nx.find_cycle(G)
                G.remove_edge(*cycle[0])
            except (nx.NetworkXError, nx.NetworkXNoCycle):
                is_cyclic = False

        return G


class RandomGraphLinearization(GraphLinearization):
    def linearize(self) -> np.ndarray:
        """Random shuffling of the nodes of the graph."""
        # discover all nodes
        sources = self.data[:, 1]
        targets = self.data[:, 2]
        nodes = np.unique(np.concatenate([sources, targets]))

        # shuffle that list
        random_index = np.random.rand(len(nodes))
        random_order = np.argsort(random_index)

        self.linearization = nodes[random_order]
        self.write_data("RandomGraph")
        return self.linearization


class BasicGraphLinearization(GraphLinearization):
    """An implementation of the naïve linearization algorithm without optimization as a basic
    proof-of-concept of using graph algorithms in the pipeline. Local neighborhoods are "sorted"
    in order of appearance of predecessors/successors to a node."""

    def linearize(self) -> np.ndarray:
        G_ = nx.from_edgelist(self.data[:, [1, 2]])

        # graph may be disconnected, so as a first step, add edges between its conn. components
        G_ = self.connect_components(G_)
        # also, these self-looping edges (node, node) break the linearization algo, so remove them
        G_.remove_edges_from(nx.selfloop_edges(G_))

        # furthermore, all cycles break this algo, so remove them
        G_ = self.remove_cycles(G_)

        G = nx.DiGraph(G_.edges)

        nodes = list(G.nodes)

        # perform the linearization algorithm, locally ordering the graph by replacing left and
        # right neighbors until all nodes have degree 2, except a start and an end with degree 1
        while (pd.DataFrame(G.degree)[1] > 2).sum() > 0:
            for node in nodes:
                left_neighbors = list(G.predecessors(node))
                in_edges = list(G.in_edges(node))

                if len(left_neighbors) > 1:
                    G.remove_edges_from(in_edges)
                    left_edges = np.empty((len(left_neighbors), 2)).astype(int)

                    left_edges[:, 0] = left_neighbors
                    left_edges[: len(left_neighbors) - 1, 1] = left_neighbors[1:]
                    left_edges[len(left_neighbors) - 1, 1] = node

                    G.add_edges_from(left_edges)

            for node in nodes:
                right_neighbors = list(G.successors(node))
                out_edges = list(G.out_edges(node))

                if len(right_neighbors) > 1:
                    G.remove_edges_from(out_edges)
                    right_edges = np.empty((len(right_neighbors), 2)).astype(int)

                    right_edges[1:, 0] = right_neighbors[0 : len(right_neighbors) - 1]
                    right_edges[:, 1] = right_neighbors
                    right_edges[0, 0] = node

                    G.add_edges_from(right_edges)

        # start and endpoint are the two nodes with degree 1
        degrees = np.array(G.degree)
        endpoints = list(degrees[degrees[:, 1] == 1][:, 0])

        self.linearization = nx.shortest_path(G, endpoints[0], endpoints[1])
        self.write_data("BasicGraph")
        return self.linearization


class WeightedGraphLinearization(GraphLinearization):
    def linearize(self) -> np.ndarray:
        """An implementation of the naïve linearization algorithm without optimization as a basic
        proof-of-concept of using graph algorithms in the pipeline. Uses node id as weights to
        "sort" the local neighborhoods."""
        G_ = nx.from_edgelist(self.data[:, [1, 2]])

        # graph may be disconnected, so as a first step, add edges between its conn. components
        G_ = self.connect_components(G_)

        # also, these self-looping edges (node, node) break the linearization algo, so remove them
        G_.remove_edges_from(nx.selfloop_edges(G_))
        G = nx.from_edgelist(G_.edges)

        latest_G = G
        nodes = list(G.nodes)

        # perform the linearization algorithm, locally ordering the graph by replacing left and
        # right neighbors until all nodes have degree 2, except a start and an end with degree 1
        while (pd.DataFrame(latest_G.degree)[1] > 2).sum() > 0:
            new_G = nx.Graph()
            new_G.nodes = G.nodes

            for node in nodes:
                neighbors = np.array(list(latest_G.neighbors(node)))
                left_neighbors = neighbors[neighbors <= node]
                right_neighbors = neighbors[neighbors > node]

                # check if node is already sorted into its neighborhood
                if len(left_neighbors) == 1 and len(right_neighbors) == 1:
                    new_G.add_edges_from(
                        [[left_neighbors[0], node], [node, right_neighbors[0]]]
                    )
                    continue

                # sort neighbors by their weight
                left_neighbors = left_neighbors[np.argsort(left_neighbors)]
                right_neighbors = right_neighbors[np.argsort(right_neighbors)]

                # left neighbors of n is an ordered list [u1, ..., ul]
                # transform this into edges [(u1, u2), (u2, u3), ..., (ul, n)]
                if len(left_neighbors) > 0:
                    left_edges = np.empty((len(left_neighbors), 2)).astype(int)

                    left_edges[:, 0] = left_neighbors
                    left_edges[: len(left_neighbors) - 1, 1] = left_neighbors[1:]
                    left_edges[len(left_neighbors) - 1, 1] = node

                    new_G.add_edges_from(left_edges)

                # right neighbors of n is an ordered list [w1, ..., wm]
                # transform this into edges [(n, w1), ..., (wm-1, wm)]
                if len(right_neighbors) > 0:
                    right_edges = np.empty((len(right_neighbors), 2)).astype(int)

                    right_edges[1:, 0] = right_neighbors[0 : len(right_neighbors) - 1]
                    right_edges[:, 1] = right_neighbors
                    right_edges[0, 0] = node

                    new_G.add_edges_from(right_edges)

            latest_G = new_G

        # start and endpoint are the two nodes with degree 1
        degrees = np.array(latest_G.degree)
        endpoints = list(degrees[degrees[:, 1] == 1][:, 0])

        self.linearization = nx.shortest_path(latest_G, endpoints[0], endpoints[1])
        self.write_data("WeightedGraph")
        return self.linearization


class SpanningTreeGraphLinearization(GraphLinearization):
    def linearize(self) -> np.ndarray:
        """Linearize the graph by traversing one of its spanning trees via depth-first search."""
        G = nx.from_edgelist(self.data[:, [1, 2]])

        # graph may be disconnected, so as a first step, add edges between its conn. components
        G = self.connect_components(G)

        # I guess you could start by computing the spanning tree?
        spanning_tree = nx.minimum_spanning_tree(G)

        # then use dfs through that tree
        dfs_tree = nx.dfs_tree(spanning_tree)
        root = list(dfs_tree.nodes)[0]
        self.linearization = np.array(
            list(nx.dfs_preorder_nodes(dfs_tree, source=root))
        )
        self.write_data("SpanningTreeGraph")
        return self.linearization


class EdgeUnawareGraphLinearization(GraphLinearization):
    def linearize(self) -> np.ndarray:
        """Sorts the nodes only based on their value (i.e., not using graph algorithms at all)."""
        G = nx.from_edgelist(self.data[:, [1, 2]])
        nodes = np.array(G.nodes)

        self.linearization = nodes[nodes.argsort()]
        self.write_data("EdgeUnawareGraph")
        return self.linearization
