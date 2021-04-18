import ast
import pandas as pd
from tokenizers import Tokenizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


def get_tfidf():
    print("Preprocessing cosine data....")
    df = pd.read_csv('./data/so_rust_lang_code.csv')
    language_tokenizer = Tokenizer.from_file('./data/language-tokenizer.json')
    # code_tokenizer = Tokenizer.from_file('./data/rust-tokenizer.json')

    # q_body_tokens = df['q_body_tokens']
    a_body_tokens = df['a_body_tokens']

    # TODO: Refactor this by saving tokens in correct format
    def tokenize(inp_str):
        return ' '.join(ast.literal_eval(inp_str))

    # q_body_tokens = q_body_tokens.apply(tokenize)
    a_body_tokens = a_body_tokens.apply(tokenize)

    a_vectorizer = TfidfVectorizer(analyzer=str.split)
    a_tfidf = a_vectorizer.fit_transform(a_body_tokens)

    # for each question, maps qid => actual question query
    qid_to_question = dict(zip(df.q_id, df.q_title))

    # maps index of question title (0,1,2...) => actual question id
    idx_to_qid = dict(zip([i for i in range(len(df))], df.q_id))

    return language_tokenizer, a_vectorizer, a_tfidf, qid_to_question, idx_to_qid


# sets global variables so we don't have to recalculate
language_tokenizer, a_vectorizer, a_tfidf, qid_to_question, idx_to_qid = get_tfidf()
