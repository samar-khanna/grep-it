import numpy as np


def so_social_update(relevant_indices, sim_scores, so_metadata):
    """
    Upweights Stack Overflow results with high answer upvote score
    :param relevant_indices: Relevant indices as returned by cosine search
    :param sim_scores: Cosine similarity scores of top results
    :param so_metadata: DataFrame with stack overflow q/a details.
    :return:
    """
    # other fields: q_view_count, q_score, a_view_count
    norm = np.linalg.norm(so_metadata['a_score'])
    scaled_norm = so_metadata['a_score'] / norm
    final_scores = scaled_norm[relevant_indices] * sim_scores[relevant_indices]
    resorted_inds = np.array(relevant_indices)[(-final_scores).argsort()]
    return resorted_inds.tolist()

# def social_update(relevant_indices, sim_scores):
#     norm = np.linalg.norm(df['a_score'])  # other fields: q_view_count, q_score,a_view_count
#     sc_norm = df['a_score'] / norm
#     final_scores = np.zeros(10)
#     for i, rel_ind in enumerate(relevant_indices):
#         final_scores[i] = (sc_norm[rel_ind]) * sim_scores[rel_ind]
#     rel_dict = {k: v for k, v in enumerate(relevant_indices)}
#     list_dict = sorted(rel_dict.items(), key=lambda x: final_scores[x[0]], reverse=True)
#     return [v for (k, v) in list_dict]


def social_update_iter(relevant_indices, relevant_indices_update, sim_scores,
                       slack=200, inv_weight=20):
    """
    given two ranking list, if sim scores are within a certain difference,
    rank according to social update rank list, otherwise rank according to first list.

    Call 2-3 times to make multiple passes over rank so not just comparing adjacent ranks.

    The "certain difference" is 1/(average sim score*slack/inv_weight).
    :param relevant_indices:
    :param relevant_indices_update:
    :param sim_scores:
    :param slack: To give less weight to social, increase slack
    :param inv_weight: decrease this to decrease range of difference for ranking rearrangment.
    :return:
    """
    final = np.zeros(len(relevant_indices))
    i = 0
    while i < len(relevant_indices):
        if i < len(relevant_indices) - 1:
            first = int(relevant_indices[i])
            second = int(relevant_indices[i + 1])
            average = (sim_scores[first] + sim_scores[second]) / 2
            difference = 1 / (average * slack / inv_weight)
            if sim_scores[first] - sim_scores[second] < difference:
                # If in the updated indices, original result i+1 appears before
                # original result i, then swap the order
                if np.where(relevant_indices_update == relevant_indices[i + 1]) < \
                        np.where(relevant_indices_update == relevant_indices[i]):
                    final[i] = relevant_indices[i + 1]
                    final[i + 1] = relevant_indices[i]
                    i += 2
                    continue
        final[i] = relevant_indices[i]
        i += 1
    return final
