# put yo similarity functions HERE to run on query with dataset
# from data.so_analyze import *
import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity
# from init_cosine import *
# from .init_tfidf import *
from .init_skipgram_embedding import *


'''
========================= cosine sim ====================================
'''


def gh_cosine_combined_embedding_search(query, query_code=None, count=5):
    query_tokens = gh_rust_tokenizer.encode(query).tokens
    if query_code is not None:
        query_tokens += gh_rust_tokenizer.encode(query_code).tokens

    query_vec = gh_rust_code_model.get_sentence_vector(' '.join(query_tokens))
    query_vec = query_vec.reshape(1, -1)

    cosine_similarities = cosine_similarity(query_vec, gh_code_vecs).flatten()

    # Get top 10 relevant results
    relevant_indices = (-cosine_similarities).argsort()[:count].tolist()

    result = gh_code_metadata.iloc[relevant_indices]
    return result


def so_social_update(relevant_indices, sim_scores):
    # other fields: q_view_count, q_score, a_view_count
    norm = np.linalg.norm(so_metadata['a_score'])
    scaled_norm = so_metadata['a_score'] / norm
    final_scores = scaled_norm[relevant_indices] * sim_scores[relevant_indices]
    resorted_inds = np.array(relevant_indices)[(-final_scores).argsort()]
    return resorted_inds.tolist()
    # final_scores = np.zeros(len(relevant_indices))
    # for i, rel_ind in enumerate(relevant_indices):
    #     final_scores[i] = (1 / sc_norm[rel_ind]) * sim_scores[rel_ind]
    # rel_dict = {k: v for k, v in enumerate(relevant_indices)}
    # list_dict = sorted(rel_dict.items(), key=lambda x: final_scores[x[0]], reverse=True)
    # return [v for (k, v) in list_dict]


def so_cosine_search(query, query_code=None, count=5):
    query_tokens = so_lang_tokenizer.encode(query).tokens
    query_lang_vec = so_lang_model.get_sentence_vector(' '.join(query_tokens))
    query_lang_vec = query_lang_vec.reshape(1, -1)

    cosine_sim = cosine_similarity(query_lang_vec, so_lang_vecs).flatten()

    if query_code is not None:
        query_code_tokens = so_code_tokenizer.encode(query_code).tokens
        query_code_vec = so_code_model.get_sentence_vector(' '.join(query_code_tokens))
        query_code_vec = query_code_vec.reshape(1, -1)

        code_cosine_sim = cosine_similarity(query_code_vec, so_code_vecs).flatten()

        # create 2D space with language and code similarites and score
        # based on distance from the origin prioritizes a high language/code score
        # over the same score between language and code
        # points = np.array([a ** 2 + b ** 2 for a, b in zip(language_cosine_sim, code_cosine_sim)])

        cosine_sim = 0.5 * cosine_sim + 0.5 * code_cosine_sim

        relevant_indices = (-cosine_sim).argsort()[:count].tolist()
    else:
        relevant_indices = (-cosine_sim).argsort()[:count].tolist()

    relevant_indices = so_social_update(relevant_indices, cosine_sim)
    return so_metadata.iloc[relevant_indices]

# # TODO: Decide whether to use combined or separate
# def so_cosine_combined_search(query, query_code=None, count=5):
#     query_tokens = so_language_tokenizer.encode(query).tokens
#     if query_code is not None:
#         query_tokens += so_code_tokenizer.encode(query_code).tokens
#
#     query_tf_idf = so_combined_vectorizer.transform([' '.join(query_tokens)])
#
#     # calculate cosine sim between docs and query
#     cosine_similarities = cosine_similarity(query_tf_idf, so_combined_tf_idf).flatten()
#
#     # Get top 10 relevant results
#     relevant_indices = (-cosine_similarities).argsort()[:count].tolist()
#
#     result = so_df.iloc[relevant_indices]
#     return result

# run cosine sim on a user query
# note: uses variables that were intially created in init_tfidf.py
# def cosine_search(query):
#     # process query
#     query_tokens = language_tokenizer.encode(query).tokens
#     query_tfidf = a_vectorizer.transform([' '.join(query_tokens)])
#
#     # calculate cosine sim between docs and query
#     cosine_similarities = cosine_similarity(query_tfidf, a_tfidf).flatten()
#     print("cosine", cosine_similarities)
#
#     # get top 10 related questions
#     related_product_indices = cosine_similarities.argsort()[:-11:-1].tolist()
#     for i in related_product_indices:
#         qid = idx_to_qid[i]
#         question = qid_to_question[qid]
#         print("QID: ", qid, "|| Question: ", question)
#
#     return [qid, question]  # sends back the first result (most similar)
