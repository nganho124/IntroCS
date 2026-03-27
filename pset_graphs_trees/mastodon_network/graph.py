from typing import List, Tuple, Optional, Union
import json
import itertools
import graphviz
import os


class User():
    def __init__(self, username):
        self.username = username

    def __str__(self):
        return self.username

    def __lt__(self, other):
        return self.username < other.username


class Graph(dict):
    """
    A graph object based on a dictionary implementation.

    Attributes:
    ----------
    sps: n*n (2-dimensional) matrix to store shortest paths between all nodes

    Methods:
    ----------
    add_vertex()
    """

    def __init__(self) -> None:
        """
        Initialize the Graph object as an empty dictionary.
        """
        super().__init__()
        self.sps = None  # Shortest path matrix, initialized as None

    def add_vertex(self, user: object) -> None:
        """
        Adds a vertex to the graph.

        Parameters:
        ----------
        user: The user object or identifier to be added as a vertex.
        """
        # Use the string representation of the user as the key
        self[user] = []

    def add_edge(self, origin: object, target: object) -> None:
        """
        Adds an edge to the graph between `origin` and `target`.

        Parameters:
        ----------
        origin: The originating vertex.
        target: The target vertex.
        """
        if origin in self.keys():
            self[origin].append(target)
            self[origin].sort()
        else:
            self[origin] = [target]
        if target in self.keys():
            self[target].append(origin)
            self[target].sort()
        else:
            self[target] = [origin]

    def remove_edge(self, edge: Tuple[object, object]) -> None:
        """
        Removes an edge from the graph.

        Parameters:
        ----------
        edge: Tuple containing the vertices that form the edge.
        """
        self[edge[0]].remove(edge[1])
        self[edge[1]].remove(edge[0])

    def remove_vertex(self, user: object) -> None:
        """
        Removes a vertex and all its edges from the graph.

        Parameters:
        ----------
        user: The user object or identifier to be removed.
        """
        del self[user]

    def dfs(self, start: object) -> List[str]:
        """
        Depth-first search starting from `start` vertex.

        Parameters:
        ----------
        start: The starting vertex.

        Returns:
        ----------
        List of visited vertices.
        """
        visited = set()
        result = []
        stack = [start]

        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                result.append(node)
                stack.extend(reversed(self[node]))

        return result

    def get_subgraphs(self) -> List[List[str]]:
        """
        Finds disconnected subgraphs (clusters) in the graph.

        Returns:
        ----------
        List of subgraphs, where each subgraph is a list of vertices.
        """
        visited = set()
        subgraphs = []

        for vertex in self.keys():
            if vertex not in visited:
                component = self.dfs(vertex)
                visited.update(component)
                subgraphs.append(component)

        return subgraphs

    def shortest_path(self, start: object, end: object) -> Union[List[str], None]:
        """
        Breadth-first search from `start` to `end` with path tracking to identify the shortest path.

        Parameters:
        ----------
        start: The starting vertex.
        end: The end vertex.

        Returns:
        ----------
        List of vertices forming the shortest path from start to end, or None if there is no path.
        """
        if start not in self or end not in self:
            return None

        if start == end:
            return [start]

        visited = set([start])
        previous = {}
        queue = [start]
        index = 0

        while index < len(queue):
            current = queue[index]
            index += 1

            for neighbor in self[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    previous[neighbor] = current

                    if neighbor == end:
                        path = [end]
                        while path[-1] != start:
                            path.append(previous[path[-1]])
                        path.reverse()
                        return path

                    queue.append(neighbor)

        # No path found
        return None

    def most_influential(self) -> Tuple[str, float]:
        """
        Identifies the most influential user based on average shortest path length.

        Returns:
        ----------
        Tuple containing the most influential user and its average shortest path length.
        """
        min_closeness = 999
        list_influence = []
        for vertex_start in self.keys():
            list_shortest_path = []
            for vertex_end in self.keys():
                if vertex_start == vertex_end:
                    continue
                path = self.shortest_path(vertex_start, vertex_end)
                if path:
                    list_shortest_path.append(len(path))

            if not list_shortest_path:
                continue
            closeness = sum(list_shortest_path) / len(list_shortest_path)

            if closeness < min_closeness:
                list_influence = [(vertex_start, closeness)]
                min_closeness = closeness
            elif closeness == min_closeness:
                list_influence.append((vertex_start, closeness))

        return list_influence

    def edge_in_sp(self, pair: Tuple[str, str], sp: List[str]) -> bool:
        """
        Checks if an edge exists in the given shortest path.

        Parameters:
        ----------
        pair: Tuple containing the users that form the edge.
        sp: The shortest path, represented as a list of vertices.

        Returns:
        ----------
        Boolean value indicating the presence of the edge in the shortest path.
        """
        # Check if the shortest path exists or is too short to contain an edge
        if not sp or len(sp) < 2:
            return False
        # Create list of edge pairs in the shortest path
        else:
            edges = list(zip(sp[:-1], sp[1:]))

        # Check if the given edge pair is in the shortest path
            if pair in edges or (pair[1], pair[0]) in edges:
                return True
            else:
                return False

    def compute_sps(self) -> None:
        """
        Computes shortest paths between every pair of nodes and stores them in `self.sps`.
        """
        # Create mappings from node keys to indices and vice versa
        nodes = list(self.keys())
        n = len(nodes)
        self.node_to_idx = {node: i for i, node in enumerate(nodes)}
        self.idx_to_node = {i: node for i, node in enumerate(nodes)}
        # Initialize the shortest paths matrix with 'None' values
        self.sps = [[None for _ in range(n)] for _ in range(n)]

        # Populate the shortest paths matrix
        for i, start in enumerate(nodes):
            for j, end in enumerate(nodes):
                if i == j:
                    self.sps[i][j] = [start]  # Path from node to itself
                else:
                    self.sps[i][j] = self.shortest_path(start, end)

    def edge_to_remove(self) -> Tuple[str, str]:
        """
        Identifies the edge to remove based on edge betweenness.

        Returns:
        ----------
        Tuple containing the vertices of the edge to remove.
        """
        # Ensure shortest paths are computed
        if self.sps is None:
            self.compute_sps()

        # Collect all unique edges (undirected)
        edges = set()
        for u in self.keys():
            for v in self[u]:
                edges.add(tuple(sorted((u, v))))

        edge_betweenness = {edge: 0 for edge in edges}

        n = len(self.sps)

        # Iterate over all shortest paths
        for i in range(n):
            for j in range(i + 1, n):  # avoid duplicates & self-pairs
                sp = self.sps[i][j]

                for edge in edges:
                    if self.edge_in_sp(edge, sp):
                        edge_betweenness[edge] += 1

        # Return edge with highest betweenness
        if not edge_betweenness:
            return None

        return max(edge_betweenness, key=edge_betweenness.get)

    def girvan_newman_algorithm(self, clusters: int) -> List[List[str]]:
        """
        Applies the Girvan-Newman algorithm to decompose the graph into specified
        number of clusters (disconnected subgraphs).

        Pseudocode for the Girvan-Newman algorithm:
        -------------------------------------------
        1. Calculate the betweenness of all existing edges in the mastodon_network.
        2. Remove the edge with the highest betweenness.
        3. Calculate the number of disconnected subgraphs.
        4. Repeat steps 1-3 until the number of disconnected subgraphs equals the predefined number of clusters.

        Parameters:
        ----------
        clusters: The number of clusters to decompose the graph into.

        Returns:
        ----------
        List of clusters, where each cluster is a list of vertices.
        """
        # Get the initial count of disconnected subgraphs
        current_clusters = self.get_subgraphs()
        num_clusters = len(current_clusters)

        # Loop until we have the desired number of clusters
        while num_clusters < clusters:
            # Compute shortest paths for all pairs of nodes
            self.compute_sps()

            # Identify the edge to be removed based on betweenness
            edge = self.edge_to_remove()

            # Check if there's an edge to remove
            if edge is None:
                # No more edges to remove, break out of loop
                break

            # Remove the identified edge
            self.remove_edge(edge)

            # Update the number of disconnected subgraphs
            current_clusters = self.get_subgraphs()
            num_clusters = len(current_clusters)

        # Return the final clusters
        return current_clusters

    def parse_data(self, filepath: str = 'ressources/graph_52n.json') -> None:
        """
        Parses graph data from a JSON file and populates the graph.

        Parameters:
        ----------
        filepath: Path to the JSON file containing the graph data.
        """
        # Open and read the JSON file
        with open(filepath, 'r') as file:
            data = json.load(file)

        # Remove the first key-item pair from data (if applicable)
        if data:
            first_key = list(data.keys())[0]
            del data[first_key]

        # Iterate over the data to populate vertices and edges
        for key, neighbors in data.items():
            key_user = User(key)

            # Add vertex for the user represented by 'key'
            self.add_vertex(key_user)

            # Add edges between 'key' and its neighbors
            for neighbor in neighbors:
                neighbor_user = User(neighbor)
                self.add_edge(key_user, neighbor_user)

    def show(self) -> None:
        """
        Generates and displays a visual representation of the graph.
        """
        # Initialize a Graphviz graph
        graph = graphviz.Graph(format='png', strict=True, filename='')

        # Add nodes to the Graphviz graph
        for node in self.keys():
            graph.node(str(node), str(node))

        # Add edges to the Graphviz graph
        for node in self.keys():
            for target in self[node]:
                graph.edge(str(node), str(target))

        # Render the graph and create a PNG file
        graph.render()

        # Remove temporary files if needed
        os.remove('')
