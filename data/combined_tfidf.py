import os
import re
import ast
import json
import numpy as np
import pandas as pd
import scipy.sparse

from sklearn.feature_extraction.text import TfidfVectorizer

from data.rust_tokenizer import add_code_tokens
from data.language_tokenizer import add_language_tokens


def create_tfidf(df):
    print("Preprocessing cosine data....")
    # qa_code_tokens = df['a_code_tokens']
    qa_tokens = pd.concat([
        df['q_title'],
        df['q_body_tokens'], df['q_code_tokens'],
        df['a_body_tokens'], df['a_code_tokens']], axis=1
    )

    # TODO: Refactor this by saving tokens in correct format
    def tokenize(inp):
        return ' '.join(inp)
        # return ' '.join(ast.literal_eval(inp_str))

    qa_tokens = qa_tokens.applymap(tokenize)
    qa_tokens = qa_tokens['q_title'] + ' ' + \
                qa_tokens['q_body_tokens'] + ' ' + \
                qa_tokens['q_code_tokens'] + ' ' + \
                qa_tokens['a_body_tokens'] + ' ' + \
                qa_tokens['a_code_tokens']

    qa_vectorizer = TfidfVectorizer(analyzer=str.split)
    qa_tfidf = qa_vectorizer.fit_transform(qa_tokens)

    return qa_vectorizer, qa_tfidf


if __name__ == "__main__":
    df = pd.read_csv('data/so_rust.csv')
    df = add_code_tokens(df, 'data/rust-tokenizer.json')
    df = add_language_tokens(df, 'data/language-tokenizer.json')

    os.makedirs('data/rust_qa_combined', exist_ok=True)

    qa_body_vectorizer, qa_tfidf = create_tfidf(df)
    with open('data/rust_qa_combined/vocab.json', 'w') as f:
        json.dump(qa_body_vectorizer.vocabulary_, f)

    np.save('data/rust_qa_combined/idf.npy', qa_body_vectorizer.idf_)

    scipy.sparse.save_npz('data/rust_qa_combined/tf_idf.npz', qa_tfidf)