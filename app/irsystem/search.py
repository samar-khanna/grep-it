# put yo similarity functions HERE to run on query with dataset
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
# from init_cosine import *
# from .init_tfidf import *
from .init_skipgram_embedding import *
from .social import so_social_update, social_update_iter


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


def so_cosine_search(query, query_code=None, count=5):
    query_tokens = so_lang_tokenizer.encode(query).tokens

    if query_code is not None:
        query_code_tokens = so_code_tokenizer.encode(query_code).tokens

        query_vec = so_model.get_sentence_vector(' '.join(query_tokens + query_code_tokens))
    else:
        query_vec = so_model.get_sentence_vector(' '.join(query_tokens))

    query_vec = query_vec.reshape(1, -1)
    cosine_sim = cosine_similarity(query_vec, so_vecs).flatten()

    relevant_indices = (-cosine_sim).argsort()[:count].tolist()

    # Update using social component
    relevant_indices_soc = so_social_update(relevant_indices, cosine_sim, so_metadata)
    for _ in range(2):
        relevant_indices = social_update_iter(relevant_indices, relevant_indices_soc,
                                              cosine_sim, slack=200, inv_weight=20)

    return so_metadata.iloc[relevant_indices]
