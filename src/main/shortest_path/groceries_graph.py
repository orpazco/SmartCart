import json
import networkx as nx
import itertools

def _build_graph():
    with open("resources/products/grocery_location.json") as f:
        data = json.load(f)

        # add node for start that represent the supermarket entrance
        data['start'] = {'aisle': 'A', 'shelf': 1}

        # Create a graph using NetworkX
        G = nx.Graph()

        # Add the grocery items as nodes to the graph
        for item, item_data in data.items():
            G.add_node(item, aisle=item_data["aisle"], shelf=item_data["shelf"])

        # Add edges between items that are in the same aisle
        for item, item_data in data.items():
            for other_item, other_item_data in data.items():
                if item != other_item:
                    weight = abs((ord(item_data["aisle"]) - ord(other_item_data["aisle"])))
                    G.add_edge(item, other_item, weight=weight)

        return G


class GroceriesGraph:
    def __init__(self):
        self.graph = _build_graph()
        self.best_path = None

    def update_shortest_path(self, items_list: []):
        best_path = None
        best_distance = float('inf')
        items_list.insert(0, 'start')
        for permutation in self._all_permutations_with_fixed_first_element(items_list):
            distance = 0
            for i in range(len(permutation) - 1):
                try:
                    path = nx.shortest_path(self.graph, permutation[i], permutation[i + 1], weight='weight')
                    distance += sum(self.graph[u][v]['weight'] for u, v in zip(path[:-1], path[1:]))
                except nx.NetworkXNoPath:
                    break
            else:
                if distance < best_distance:
                    best_distance = distance
                    best_path = permutation
        self.best_path = best_path

    def to_string(self):
        sb = []
        for i in range(len(self.best_path) - 1):
            sb.append(" {0}: {1}  →".format(self.best_path[i], self._aisle_and_self(self.best_path[i])))
        sb.append(" {0}: {1}".format(self.best_path[-1], self._aisle_and_self(self.best_path[-1])))
        return "".join(sb)

    def _all_permutations_with_fixed_first_element(self, lst):
        first_element = lst[0]
        permutations = list(itertools.permutations(lst))
        return [p for p in permutations if p[0] == first_element]

    def _aisle_and_self(self, node):
        node_location = self.graph.nodes.get(node)
        return "{}{}".format(node_location['aisle'], node_location['shelf'])

graph = GroceriesGraph()