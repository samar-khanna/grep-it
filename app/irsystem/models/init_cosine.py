import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity


def cosine_data():
    print("Preprocessing cosine data....")
    #df = pd.read_csv ('../../../data/so_rust.csv')
    df = pd.read_csv ('./data/so_rust.csv')
    titles = df['q_title'].to_dict()
    qidToQuestion = dict(zip(df.q_id, df.q_title)) #for each question, maps qid => actual question query

    # get train/test set from data (question titles for now)
    docs = list(titles.values())
    train = docs[:len(docs)-10]
    test = docs[len(docs)-10:]

    #maps index of question title (0,1,2...) to actual question id
    idxToQid = dict(zip([i for i in range(len(docs))], df.q_id)) #idx of question title (0,1,..) => actual question id

    #creates tf-idf
    tfIdfVectorizer=TfidfVectorizer(use_idf=True)
    tfidf = tfIdfVectorizer.fit_transform(docs) #using all docs for now
    similarity_matrix = cosine_similarity(tfidf, tfidf)

    return tfidf, tfIdfVectorizer, qidToQuestion, idxToQid #create once

#sets global variables so we don't have to recalculate
tfidf, tfIdfVectorizer, qidToQuestion, idxToQid = cosine_data()

