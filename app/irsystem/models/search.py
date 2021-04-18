#put yo similarity functions HERE to run on query with dataset
from data.so_analyze import *
import pandas as pd
import numpy as np
import re

def jaccard_sim(query_lst, question_lst):
    inter = len(list(set(query_lst).intersection(question_lst)))
    union = (len(query_lst) + len(question_lst)) - inter
    return float(inter) / union

def tokenize(str):
    return str.split()

def test(query, dataset=[]):
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


