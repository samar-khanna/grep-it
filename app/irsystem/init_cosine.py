import ast
import json
import numpy as np
import pandas as pd
from scipy.sparse import load_npz

from tokenizers import Tokenizer
from sklearn.feature_extraction.text import TfidfVectorizer


def init_tfidf_vectorizer(path_to_vocab, path_to_idf, path_to_tfidf):
    # Load the Tfidf vocab counts and the idf array
    with open(path_to_vocab) as f:
        vocab = json.load(f)
    idf = np.load(path_to_idf)

    vectorizer = TfidfVectorizer(analyzer=str.split)
    vectorizer.vocabulary_ = vocab
    vectorizer.idf_ = idf

    tf_idf = load_npz(path_to_tfidf)

    return vectorizer, tf_idf


# sets global variables so we don't have to recalculate
df = pd.read_csv('./data/so_rust.csv')

language_tokenizer = Tokenizer.from_file('./data/language-tokenizer.json')
code_tokenizer = Tokenizer.from_file('./data/rust-tokenizer.json')

# Load the body Tfidf vocab counts and the idf array
language_vectorizer, language_tf_idf = init_tfidf_vectorizer(
    './data/rust_qa_body/vocab.json',
    './data/rust_qa_body/idf.npy',
    './data/rust_qa_body/tf_idf.npz'
)

code_vectorizer, code_tf_idf = init_tfidf_vectorizer(
    './data/rust_qa_code/vocab.json',
    './data/rust_qa_code/idf.npy',
    './data/rust_qa_code/tf_idf.npz'
)

# TODO: Determine if this is useful
combined_vectorizer, combined_tf_idf = init_tfidf_vectorizer(
    './data/rust_qa_combined/vocab.json',
    './data/rust_qa_combined/idf.npy',
    './data/rust_qa_combined/tf_idf.npz'
)

# for each question, maps qid => actual question query
qid_to_question = dict(zip(df.q_id, df.q_title))

# maps index of question title (0,1,2...) => actual question id
idx_to_qid = dict(zip([i for i in range(len(df))], df.q_id))

# language_tokenizer, a_vectorizer, a_tfidf, qid_to_question, idx_to_qid = get_tfidf()