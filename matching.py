import matching_helpers
import helpers
import itertools
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize as Norm

def find_matchings(matching_size, low_maxes, high_mins, step):

    all_concepts = range(len(helpers.allConcepts))
    concept_combos = list(itertools.combinations(all_concepts, matching_size))

    array_height = round((low_maxes[1] - low_maxes[0]) / step + 1)
    array_width = round((high_mins[1] - high_mins[0]) / step + 1)
    results_array = [[[] for _ in range(array_width)] for _ in range(array_height)]
    results_list = []

    count_array = [[0 for _ in range(array_width)] for _ in range(array_height)]
    diff_array = [[[] for _ in range(array_width)] for _ in range(array_height)]



    for i in range(array_height):
        for j in range(array_width):
            print(i, j)
            for concept_combo in concept_combos:
                my_matchings = matching_helpers.has_valid_matching(concept_combo,
                                                                  [low_maxes[0], low_maxes[0] + step * i],
                                                                  [high_mins[0] + step * j, high_mins[1]])
                if my_matchings:
                    for my_matching in my_matchings:
                        results_array[i][j].append(my_matching)
                        results_list.append(my_matching)

                        """count_array[i][j] += 1
                        diff_array[i][j].append(my_matching.delta_es_diff())

    for i in range(array_height):
        for j in range(array_width):
            if diff_array[i][j]:
                diff_array[i][j] = sum(diff_array[i][j]) / len(diff_array[i][j])
            else:
                diff_array[i][j] = 300

    plt.close()
    plt.imshow(diff_array)
    plt.show()"""
    results_list.sort(key=lambda x: x.delta_es_diff())

    for i in range(100):
        print(results_list[i].delta_es_diff())

    matching_helpers.display_matching(results_list[0])

    return (results_array, results_list)


find_matchings(4, [0, 0.45], [0.55, 1], 0.05)