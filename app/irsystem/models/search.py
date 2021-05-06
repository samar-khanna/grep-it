# put yo similarity functions HERE to run on query with dataset
# from data.so_analyze import *
import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity
# from init_cosine import *
from .init_cosine import *

'''
========================= jaccard ====================================
'''


def jaccard_sim(query_lst, question_lst):
    inter = len(list(set(query_lst).intersection(question_lst)))
    union = (len(query_lst) + len(question_lst)) - inter
    return float(inter) / union


def tokenize(str):
    return str.split()


def jaccard_search(query, dataset=[]):
    # sample simple jaccard sim between query and questions in df
    q_df = df[['q_id', 'q_title']]
    # create array of size 1 X number of questions to store jaccard sim score between query and that question
    j_sim = np.zeros(27498)
    for j_sim_index in range(27498):
        j_sim[j_sim_index] = jaccard_sim(tokenize(query), tokenize(q_df['q_title'][j_sim_index]))
    max_index = np.argmax(j_sim)
    # get the full q & a pair from the df
    # print(df.iloc[max_index])
    return [df['q_title'][max_index],
            df['a_body'][max_index]]  # returns [question, answer body] pair with highest score


'''
========================= cosine sim ====================================
'''


#separate works better rn
def cosine_combined_search(query, query_code=None):
    query_tokens = language_tokenizer.encode(query).tokens
    if query_code is not None:
        query_tokens += code_tokenizer.encode(query_code).tokens

    query_tf_idf = combined_vectorizer.transform([' '.join(query_tokens)])

    # calculate cosine sim between docs and query
    cosine_similarities = cosine_similarity(query_tf_idf, combined_tf_idf).flatten()

    # Get top 10 relevant results
    relevant_indices = (-cosine_similarities).argsort()[:10].tolist()

    result = df.iloc[relevant_indices]
    return result


def cosine_search(query, query_code=None):
    query_tokens = language_tokenizer.encode(query).tokens
    query_tf_idf = language_vectorizer.transform([' '.join(query_tokens)])
    language_cosine_sim = cosine_similarity(query_tf_idf, language_tf_idf).flatten()

    if query_code is not None:
        query_code_tokens = code_tokenizer.encode(query_code).tokens
        query_code_tf_idf = code_vectorizer.transform([' '.join(query_code_tokens)])
        code_cosine_sim = cosine_similarity(query_code_tf_idf, code_tf_idf).flatten()

        # create 2D space with language and code similarites and score
        # based on distance from the origin prioritizes a high language/code score
        # over the same score between language and code
        points = np.array([a ** 2 + b ** 2 for a, b in zip(language_cosine_sim, code_cosine_sim)])

        relevant_indices = (-points).argsort()[:10].tolist()
        #print(relevant_indices)
         #norm of scores length of all posts
        relevant_indices_social = social_update(relevant_indices,points)
        #print(relevant_indices_social)
        relevant_indices_merge_1=social_update_2(relevant_indices,relevant_indices_social, points)
        #print(relevant_indices_merge_1)
        relevant_indices_merge_2=social_update_2(relevant_indices_merge_1,relevant_indices_social, points)
        #print(relevant_indices_merge_2)
    else:
        relevant_indices = (-language_cosine_sim).argsort()[:10].tolist()
        #print(relevant_indices)
        relevant_indices_social = social_update(relevant_indices,language_cosine_sim)
        #print(relevant_indices_social)
        relevant_indices_merge_1=social_update_2(relevant_indices,relevant_indices_social, language_cosine_sim)
        #print(relevant_indices_merge_1)
        relevant_indices_merge_2=social_update_2(relevant_indices_merge_1,relevant_indices_social, language_cosine_sim)
        #print(relevant_indices_merge_2)
    return df.iloc[relevant_indices_merge_2]

def social_update(relevant_indices, sim_scores):
    norm = np.linalg.norm(df['a_score']) #other fields: q_view_count, q_score,a_view_count
    sc_norm=df['a_score']/norm
    final_scores=np.zeros(10)
    for i, rel_ind in enumerate(relevant_indices):
        final_scores[i]=(sc_norm[rel_ind])*sim_scores[rel_ind]
    rel_dict = {k: v for k,v in enumerate(relevant_indices)}
    list_dict=sorted(rel_dict.items(), key= lambda x: final_scores[x[0]], reverse=True)
    return [v for (k,v) in list_dict]

def social_update_2(relevant_indices, relevant_indices_update, sim_scores):
    #given two ranking list, if sim scores are within a certain difference, rank according to social update rank list, otherwise rank according to first list
    #call this function 2-3times to make multiple passes over rank so not just comparing adjacent ranks
    #the "certain difference" is 1/(average sim score*slack/inv_weight), to give less weight to social, decrease inv_weight
    #to decrease range of difference for ranking rearrangment, increase slack
    slack=200
    inv_weight=20
    final=np.zeros(10)
    i=0
    while i<10:
        if i!=9:
            first=int(relevant_indices[i])
            second=int(relevant_indices[i+1])
            average=(sim_scores[first]+sim_scores[second])/2
            difference=1/(average*slack/inv_weight)
            if (sim_scores[first]-sim_scores[second]<difference):
                if np.where(relevant_indices_update == relevant_indices[i+1]) < np.where(relevant_indices_update == relevant_indices[i]) :
                    final[i]=relevant_indices[i+1]
                    final[i+1]=relevant_indices[i]
                    i+=2
                else:
                    final[i]=relevant_indices[i]
                    i+=1
            else:
                final[i]=relevant_indices[i]
                i+=1
        else:
            final[i]=relevant_indices[i]
            i+=1
    return final

# run cosine sim on a user query
# note: uses variables that were intially created in init_cosine.py
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
