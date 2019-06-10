import matching_helpers
import helpers
import itertools
from matplotlib import pyplot as plt
import numpy as np
import math

def find_matchings(matching_size, low_maxes, high_mins, step):

    all_concepts = range(len(helpers.allConcepts))
    concept_combos = list(itertools.combinations(all_concepts, matching_size))

    array_height = round((low_maxes[1] - low_maxes[0]) / step + 1)
    array_width = round((high_mins[1] - high_mins[0]) / step + 1)
    results_array = [[[] for _ in range(array_width)] for _ in range(array_height)]
    results_list = []

    count_array = [[0 for _ in range(array_width)] for _ in range(array_height)]
    diff_array = [[[] for _ in range(array_width)] for _ in range(array_height)]
    min_diff_array = [[0 for _ in range(array_width)] for _ in range(array_height)]

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

                        count_array[i][j] += 1
                        diff_array[i][j].append(my_matching.delta_es_diff())

    for i in range(array_height):
        for j in range(array_width):
            if diff_array[i][j]:
                min_diff_array[i][j] = min(diff_array[i][j])
            else:
                min_diff_array[i][j] = math.inf

    for i in range(array_height):
        for j in range(array_width):
            if diff_array[i][j]:
                diff_array[i][j] = sum(diff_array[i][j]) / len(diff_array[i][j])
            else:
                diff_array[i][j] = math.inf

    # https://matplotlib.org/3.1.0/gallery/images_contours_and_fields/image_annotated_heatmap.html
    # Tweak + step if getting display errors
    low_ranges = ["[" + str(low_maxes[0]) + ", " + str.format('{0:.2f}', i) + "]"
                  for i in np.arange(low_maxes[0], low_maxes[1] + step, step)]
    high_ranges = ["[" + str.format('{0:.2f}', i) + ", " + str(high_mins[1]) + "]"
                   for i in np.arange(high_mins[0], high_mins[1] + step, step)]

    fig, ax = plt.subplots()
    # show all ticks
    ax.set_yticks(np.arange(len(low_ranges)))
    ax.set_xticks(np.arange(len(high_ranges)))
    # label ticks
    ax.set_yticklabels(low_ranges)
    ax.set_xticklabels(high_ranges)
    plt.xlabel("'Strong' Association Range")
    plt.ylabel("'Weak' Association Range")

    # Number of Valid Matchings
    """im = ax.imshow(count_array)

    # Loop over data dimensions and create text annotations.
    for i in range(len(low_ranges)):
        for j in range(len(high_ranges)):
            text = ax.text(j, i, count_array[i][j],
                           ha="center", va="center", color="w")

    ax.set_title("Number of Valid Matchings")

    fig.tight_layout()
    plt.show()"""

    # Average Difference
    """im = ax.imshow(diff_array)

    # Loop over data dimensions and create text annotations.
    for i in range(len(low_ranges)):
        for j in range(len(high_ranges)):
            text = ax.text(j, i, str.format('{0:.2f}', diff_array[i][j]),
                           ha="center", va="center", color="w")

    ax.set_title("Average (Max Delta E - Min Delta E) per Matching")

    fig.tight_layout()
    plt.show()"""

    # Min Difference
    im = ax.imshow(min_diff_array)

    # Loop over data dimensions and create text annotations.
    for i in range(len(low_ranges)):
        for j in range(len(high_ranges)):
            text = ax.text(j, i, str.format('{0:.2f}', min_diff_array[i][j]),
                           ha="center", va="center", color="w")

    ax.set_title("Min(Max Delta E - Min Delta E)")

    fig.tight_layout()
    plt.show()


    # results_list.sort(key=lambda x: x.delta_es_diff())

    # matching_helpers.display_matching(results_list[0])

    """strong_results = results_array[6][3]
    strong_results.sort(key=lambda x: x.delta_es_diff())
    for result in strong_results:
        print(result.delta_es_diff())
    matching_helpers.display_matching(strong_results[0])

    return (results_array, results_list)"""


find_matchings(4, [0, 0.45], [0.55, 1], 0.05)