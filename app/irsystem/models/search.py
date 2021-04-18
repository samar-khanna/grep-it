#put yo similarity functions HERE to run on query with dataset
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
    df = pd.read_csv ('./data/so_rust.csv')
    #sample simple jaccard sim between query and questions in df
    q_df= df[['q_id', 'q_title']]
    #create array of size 1 X number of questions to store jaccard sim score between query and that question
    j_sim=np.zeros(27498)
    for j_sim_index in range(27498):
        j_sim[j_sim_index]=jaccard_sim(tokenize(query),tokenize(q_df['q_title'][j_sim_index]))
    max_index= np.argmax(j_sim)
    #get the full q & a pair from the df
    #print(df.iloc[max_index])
    return [df['q_title'][max_index], df['a_body'][max_index]] #returns [question, answer body] pair with highest score


'''
========================= cosine sim ====================================
'''

# run cosine sim on a user query
# note: uses variables that were intially created in init_cosine.py
def cosine_sim(query):
    # process query
    words = tfIdfVectorizer.get_feature_names() #returns words
    queryTFIDF = TfidfVectorizer().fit(words)
    queryTFIDF = queryTFIDF.transform([query])

    #calculate cosine sim between docs and query
    cosine_similarities = cosine_similarity(queryTFIDF, tfidf).flatten()
    print("cosine", cosine_similarities)

    # get top 10 related questions
    related_product_indices = cosine_similarities.argsort()[:-11:-1].tolist()
    for i in related_product_indices:
        qid = idxToQid[i]
        question = qidToQuestion[qid]
        print("QID: ", qid, "|| Question: ", question)
    
    max_indx = 0
    return [qid, question] #sends back the first result (most similar)


# tfidf, tfIdfVectorizer, qidToQuestion, idxToQid = cosine_data()
# cosine_sim("query")

