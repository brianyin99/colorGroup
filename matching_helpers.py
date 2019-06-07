import helpers
from skimage import color as clr
import networkx as nx


class Matching:
    def __init__(self, concepts, colors, max_low, min_high):
        self.concepts = concepts
        self.colors = colors
        self.max_low = max_low
        self.min_high = min_high

    def my_graph(self):
        """Weighted bipartite graph of matching"""
        B = nx.Graph()
        B.add_nodes_from(self.concepts, bipartite=0)
        B.add_nodes_from(self.colors, bipartite=1)
        for concept in self.concepts:
            for color in self.colors:
                B.add_edge(concept, color, weight=helpers.data[concept][color])
        return B

    def all_delta_es(self):
        """Compute delta E between each pair of colors"""
        delta_e_list = []
        for i in range(len(self.colors)):
            for j in range(i + 1, len(self.colors)):
                delta_e_list.append(clr.deltaE_ciede2000(self.colors[i], self.colors[j]))
        return delta_e_list

    def delta_es_diff(self):
        """Return max value - min value for all_delta_es"""
        delta_e_list = self.all_delta_es
        return max(delta_e_list) - min(delta_e_list)



my_concepts = [0, 1, 2, 3]
high_range = [0.55, 1]
low_range = [0, 0.45]

color_ratings = helpers.data
color_values = helpers.colorData
colors_remaining = color_values.copy()

final_pairings = {}


# for each color, discard color unless highly associated with exactly one concept and weakly associated with the rest
for i in range(len(color_values)):
    my_color = color_values[i]

    # discard color unless highly associated with exactly one concept
    num_high_assoc = 0
    high_concept = None
    for concept_index in my_concepts:
        color_assoc = color_ratings[concept_index][i]
        if color_assoc >= high_range[0] and color_assoc <= high_range[1]:
            high_concept = concept_index
            num_high_assoc += 1
    if not num_high_assoc == 1:
        colors_remaining.remove(my_color)
        continue

    # discard color unless weakly associated with remaining concepts
    concepts_passed = 0
    for concept in my_concepts:
        if not concept == high_concept:
            if not (color_ratings[concept][i] >= low_range[0] and color_ratings[concept][i] <= low_range[1]):
                colors_remaining.remove(my_color)
                break
            else:
                concepts_passed += 1
        if concepts_passed == len(my_concepts) - 1:
            if high_concept in final_pairings:
                final_pairings[high_concept].append(my_color)
            else:
                final_pairings[high_concept] = [my_color]
            print(helpers.allConcepts[high_concept])
