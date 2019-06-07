import helpers



my_concepts = [0, 3, 9, 6]
high_range = [0.5, 1]
low_range = [0, 0.4]

color_ratings = helpers.data
color_values = helpers.colorData
colors_remaining = color_values.copy()


# for each color, discard color unless highly associated with exactly one concept and weakly associated with the rest
for i in range(len(color_values)):

    # discard color unless highly associated with exactly one concept
    num_high_assoc = 0
    high_concept = None
    for concept_index in my_concepts:
        color_assoc = color_ratings[concept_index][i]
        if color_assoc >= high_range[0] and color_assoc <= high_range[1]:
            high_concept = concept_index
            num_high_assoc += 1
    if not num_high_assoc == 1:
        colors_remaining.remove(color_values[i])
        continue


    # discard color unless weakly associated with remaining concepts
    for concept in my_concepts:
        if not concept == high_concept:
            if not (color_ratings[concept][i] >= low_range[0] and color_ratings[concept][i] <= low_range[1]):
                colors_remaining.remove(color_values[i])
                break

    print(helpers.allConcepts[high_concept])






print('done')