import helpers
from skimage import color as clr
import networkx as nx
import matplotlib.pyplot as plt
import itertools


class Matching:
    def __init__(self, concepts, colors, low_range, high_range):
        self.concepts = concepts
        self.colors = [helpers.colorData.index(color) for color in colors]
        self.low_range = low_range
        self.high_range = high_range

        B = nx.Graph()
        B.add_nodes_from(self.concepts, bipartite=0)
        B.add_nodes_from(self.colors, bipartite=1)
        for concept in self.concepts:
            for color in self.colors:
                B.add_edge(concept, color, weight=helpers.data[concept][color])


        self.my_graph = B

    def all_delta_es(self):
        """Compute delta E between each pair of colors"""
        delta_e_list = []
        for i in range(len(self.colors)):
            for j in range(i + 1, len(self.colors)):
                delta_e_list.append(clr.deltaE_ciede2000(helpers.colorData[self.colors[i]], helpers.colorData[self.colors[j]]))
        return delta_e_list

    def delta_es_diff(self):
        """Return max value - min value for all_delta_es"""
        delta_e_list = self.all_delta_es()
        return max(delta_e_list) - min(delta_e_list)

def has_valid_matching(my_concepts, low_range, high_range):
    """Returns a dictionary of all valid matching(s) or False"""

    color_ratings = helpers.data
    color_values = helpers.colorData
    final_pairings = {} # (concept, [LAB value(s)])

    # for each color, discard color unless highly associated with exactly one concept and weakly associated with the rest
    for i in range(len(color_values)):
        my_color = color_values[i]

        # color should be highly associated with one concept
        num_high_assoc = 0
        high_concept = None
        for concept_index in my_concepts:
            color_assoc = color_ratings[concept_index][i]
            if color_assoc >= high_range[0] and color_assoc <= high_range[1]:
                high_concept = concept_index
                num_high_assoc += 1
        if num_high_assoc == 1:

            # color should be weakly associated with remaining concepts
            concepts_passed = 0
            for concept in my_concepts:
                if not concept == high_concept:
                    if color_ratings[concept][i] >= low_range[0] and color_ratings[concept][i] <= low_range[1]:
                        concepts_passed += 1
            if concepts_passed == len(my_concepts) - 1:
                if high_concept in final_pairings:
                    final_pairings[high_concept].append(my_color)
                else:
                    final_pairings[high_concept] = [my_color]

    # if some concept does not have a color, return False
    if False in [concept in final_pairings for concept in my_concepts]:
        return False
    # compute all possible matchings
    else:
        # list of all matching combinations
        # https://codereview.stackexchange.com/questions/171173/list-all-possible-permutations-from-a-python-dictionary-of-lists
        all_matchings = []
        keys, values = zip(*final_pairings.items())
        all_matching_dicts = [dict(zip(keys, v)) for v in itertools.product(*values)] # [{concept: LAB value, concept: LAB value, etc.}]
        for matching in all_matching_dicts:
            all_matchings.append(Matching(list(matching.keys()), list(matching.values()), low_range, high_range))

        return all_matchings


def display_matching(my_matching):
    """Display the graph representation of a Matching instance"""
    G = my_matching.my_graph

    # set positions of nodes (concepts along the top, colors along the bottom)
    pos = {}
    pos.update((node, (my_matching.concepts.index(node), 2)) for node in my_matching.concepts)
    pos.update((node, (my_matching.colors.index(node), 1)) for node in my_matching.colors)
    weights = [G[u][v]['weight'] for u,v in G.edges]

    # labels for nodes
    labels = {}
    for node in my_matching.concepts:
        labels[node] = helpers.allConcepts[node]
    for node in my_matching.colors:
        labels[node] = helpers.colorData[node]

    # positions of labels
    pos_higher = {}
    pos_higher.update((node, (my_matching.concepts.index(node), 2.05)) for node in my_matching.concepts)
    pos_higher.update((node, (my_matching.colors.index(node), 0.95)) for node in my_matching.colors)

    # use RGB color to display color nodes
    values = [clr.lab2rgb([[helpers.colorData[node]]])[0][0].tolist() for node in my_matching.colors]

    nx.draw(G, pos=pos, width=weights)
    nx.draw_networkx_labels(G, pos_higher, labels=labels)
    nx.draw_networkx_nodes(G, pos=pos, nodelist=my_matching.concepts, node_color='w', edgecolors='k', node_size=400)
    nx.draw_networkx_nodes(G, pos=pos, nodelist=my_matching.colors, node_color=values, node_shape='s', node_size=500)

    # display weight along edges
    # https://stackoverflow.com/questions/28957286/how-to-remove-an-attribute-from-the-edge-label-in-a-networkx-graph
    labels = {}
    for u, v, data in G.edges(data=True):
        labels[(u, v)] = str.format('{0:.3f}', data['weight'])


    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=labels, label_pos=0.8)

    plt.show()


# test values
"""my_concepts = [0, 1, 2, 3]
high_range = [0.55, 1]
low_range = [0, 0.45]
test_matching = has_valid_matching(my_concepts, low_range, high_range)[7]
display_matching(test_matching)




print('done')"""
